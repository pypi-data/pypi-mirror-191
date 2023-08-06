from typing import Any, BinaryIO, Dict, Optional, Union
from ml4data.base import ML4DataClient
from PIL import Image
from io import BytesIO

ImageType = Union[str, Image.Image, BinaryIO]

class VisionClient(ML4DataClient):
    base_url = ML4DataClient.base_url + '/vision'

    def _send_image(self,
                    endpoint: str,
                    img: Optional[ImageType] = None,
                    url: Optional[str] =None) -> Any:
        if (img is None and url is None) or (img is not None and url is not None):
            raise ValueError("Pass either a path, file handler, Pillow image or url as argument")

        if img is not None:
            if isinstance(img, str):
                with open(img, 'rb') as fp:
                    r = self._post(endpoint=endpoint,
                                   files={'file': fp})
            elif isinstance(img, Image.Image):
                b = BytesIO()
                img.save(b, 'png')
                b.seek(0)
                r = self._post(endpoint=endpoint,
                               files={'file': b})
            else: # file-like
                r = self._post(endpoint=endpoint,
                               files={'file': img})
        else: # url is not None:
            r = self._get(endpoint=endpoint,
                          params={'url': url})
        return r

    def detect_object(self,
                      img: Optional[ImageType] = None,
                      url: Optional[str] = None) -> Dict:
        """ Detect objects in an image

        Pass either one of img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/object-detection',
                                img=img,
                                url=url)

    def detect_facemask(self,
                        img: Optional[ImageType] = None,
                        url: Optional[str] = None) -> Dict:
        """ Detect face maks in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/facemask-detection',
                                img=img,
                                url=url)

    def classify_product(self,
                         img: Optional[ImageType] = None,
                         url: Optional[str] = None) -> Dict:
        """ Classify the main product in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/products',
                                img=img,
                                url=url)

    def ocr(self,
            img: Optional[ImageType] = None,
            url: Optional[str] = None) -> Dict:
        """ Extract text from an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/ocr',
                                img=img,
                                url=url)

    def colors(self,
               img: Optional[ImageType] = None,
               url: Optional[str] = None) -> Dict:
        """ Find main colors in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/colors',
                                img=img,
                                url=url)
