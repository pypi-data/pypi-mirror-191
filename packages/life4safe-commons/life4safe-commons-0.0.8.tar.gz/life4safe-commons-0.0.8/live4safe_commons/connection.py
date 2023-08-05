import pika
import sys
import os
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from pathlib import Path
import logging
from live4safe_commons.liveness_status_enum import LivenessStatusEnum

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

UPDATE_URL = os.getenv("UPDATE_URL", "http://localhost:8000/liveness/")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

logger.info("Environment Variables:")
logger.info(UPDATE_URL)
logger.info(RABBITMQ_HOST)
logger.info(RABBITMQ_PORT)


class Connection:
    video_path = None
    port = None
    choosen_method = None
    connection = None
    channel = None
    current_method = None

    def __init__(self, cho_method, cur_method):
        logger.info(f'Initiating {cho_method}...')
        self.choosen_method = cho_method

        try:
            Path("./videos").mkdir(parents=True, exist_ok=True)
            self.current_method = cur_method

        except SystemExit:
            os._exit(0)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
            del self.connection
            del self.channel
        pth = Path("./videos")
        for file in pth.iterdir():
            file.unlink()
        pth.rmdir()
        del pth

    def set_route(self):
        try:
            logger.info(
                f'Connecting Pika to {RABBITMQ_HOST} at port {RABBITMQ_PORT}')
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.choosen_method)

        except Exception as ex:
            logger.error(
                f'Connecting Pika to {RABBITMQ_HOST} at port {RABBITMQ_PORT}')
            logger.exception(ex)
            logger.critical("Aborting...")
            exit()

    def callback(self, ch, method, properties, body):
        logger.info("Method: {}".format(self.choosen_method))
        logger.info("Analysing Video: {}".format(body.decode("utf-8")))
        message = json.loads(body.decode("utf-8"))
        answer = {}
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[492, 500, 502, 503, 504 ])
        session = requests.Session()
        session.mount('https://',HTTPAdapter(max_retries=retries))
        session.mount('http://',HTTPAdapter(max_retries=retries))
        url_callback = f'{UPDATE_URL}{message.get("liveness_id")}/'
        try:
            # Download video file from video_path in Google Storage
            logger.info("Downloading video from Bucket")
            pth = "./videos/" + str(message["video_path"]).split("/")[-1]
            header = {"Authorization": message.get("token")}
            r = session.get(message["video_path"], allow_redirects=True)
            if r.ok:
                with open(pth, "wb") as target:
                    target.write(r.content)
                # PROCESS VIDEO                
                session.patch(url=url_callback,
                    headers=header,
                    json={
                        f"{self.choosen_method}_status": 
                        LivenessStatusEnum.processing.name}
                )
                #logger.info("Starting Liveness method: {}".format(self.choosen_method))
                answer = self.current_method.analyse_video(pth)
                
                logger.info("Finishing Liveness method.")
                """"
                logger.info(
                    "Finishing Liveness method: {}, ANSWER: {}"
                    .format(self.choosen_method, answer))
                """
                # Delete downloaded file after processing
                Path(pth).unlink()
                session.patch(url=url_callback,
                               headers=header,
                               json=answer)
            else:
                logger.error(
                    "Video %s was not found on server, aborting processing...",
                    str(message["video_path"]).split("/")[-1],
                )
                session.put(
                    url=url_callback,
                    headers=header,
                    json={
                        f"{self.choosen_method}_status":
                        LivenessStatusEnum.error.name},
                )

        except Exception as ex:
            logger.exception(
                "An exception ocurred when trying to process video: %s",
                ex
            )
            session.put(
                url=url_callback,
                headers=header,
                json={
                    f"{self.choosen_method}_status":
                    LivenessStatusEnum.execption.name},
            )

    def get_request(self):
        try:
            # os.system("cls" if os.name == "nt" else "clear")
            logger.info("Setting Route")
            self.set_route()

            logger.info("Start consuming")
            self.channel.basic_consume(
                queue=self.choosen_method,
                on_message_callback=self.callback,
                auto_ack=True,
            )
            print("\n\n[*] Waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Interrupted")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
