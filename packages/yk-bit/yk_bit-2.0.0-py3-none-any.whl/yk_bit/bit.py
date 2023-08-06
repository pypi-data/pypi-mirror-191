""" Module of the Youverse BiometricInThings API.
"""
from enum import Enum
from yk_utils.images import parse_image
from yk_utils.apis import request, YoonikApiException
from yk_bit_api_models import CaptureRequest, VerifyImagesRequest, VerifyRequest, \
    CaptureResponse, VerifyResponse, VerifyImagesResponse, HardwareResetResponse


class BiTStatus(Enum):
    NotAvailable = 0
    Available = 1


def capture(capture_timeout: float = 10, anti_spoofing: bool = True,
            live_quality_analysis: bool = False) -> CaptureResponse:
    """ Provides a live captured frame from the devices camera in base 64 format and its quality metrics.
    :param capture_timeout:
        Capture timeout in seconds.
    :param anti_spoofing:
        Activates anti-spoofing detection.
    :param live_quality_analysis:
        Activate ISO/ICAO-19794-5 face quality compliance checks on the live face images.
    :return:
        The captured image in base 64 format and the capture status.
    """

    url = 'bit/capture'
    capture_request = CaptureRequest(capture_timeout, anti_spoofing, live_quality_analysis).to_dict()
    response = request('POST', url, json=capture_request)

    return CaptureResponse.from_dict(response)


def verify(reference_image, capture_time_out: float = 10.0, matching_score_threshold: float = 0.4,
           anti_spoofing: bool = True, live_quality_analysis: bool = False,
           reference_quality_analysis: bool = False) -> VerifyResponse:
    """ Captures a live frame from the camera and cross examines with the reference image.
        :param reference_image:
            Image can be a string, a file path or a file-like object.
        :param reference_quality_analysis:
            Activate ISO/ICAO-19794-5 face quality compliance checks on the image.
        :param live_quality_analysis:
            Activate ISO/ICAO-19794-5 face quality compliance checks on the live face images.
        :param anti_spoofing:
            Activate anti-spoofing detection.
        :param matching_score_threshold:
            Defines the minimum acceptable score for a positive match.
        :param capture_time_out:
            Capture timeout in seconds.
        :return:
            The frame that was captured to verify against the reference in base 64 format,
             its verification status and the matching score.
        """
    url = 'bit/verify'
    verify_request = VerifyRequest(
        reference_image=parse_image(reference_image),
        capture_time_out=capture_time_out,
        matching_score_threshold=matching_score_threshold,
        anti_spoofing=anti_spoofing,
        live_quality_analysis=live_quality_analysis,
        reference_quality_analysis=reference_quality_analysis,
    ).to_dict()

    response = request('POST', url, json=verify_request)

    return VerifyResponse.from_dict(response)


def verify_images(probe_image, reference_image, matching_score_threshold: float = 0.4) \
        -> VerifyImagesResponse:
    """ Performs face matching between the two provided images.
    :param matching_score_threshold:
        Defines the minimum acceptable score for a positive match.
    :param probe_image:
        Image can be a string or a file path or a file-like object.
    :param reference_image:
        Image can be a string or a file path or a file-like object.
    :return:
        The matching score and the verified images status.
    """
    url = 'bit/verify_images'
    verify_images_request = VerifyImagesRequest(
        probe_image=parse_image(probe_image),
        reference_image=parse_image(reference_image),
        matching_score_threshold=matching_score_threshold
    ).to_dict()

    response = request('POST', url, json=verify_images_request)

    return VerifyImagesResponse.from_dict(response)


def hardware_reset() -> HardwareResetResponse:
    """ Performs camera hardware reset.
    :return:
        The hardware reset response.
    """
    url = 'bit/hardware_reset'
    try:
        response = request('POST', url)
    except YoonikApiException as yk_exc:
        if yk_exc.status_code == 501:
            return HardwareResetResponse(message="Hardware reset not implemented "
                                                 "for the installed camera type.")
    return HardwareResetResponse.from_dict(response)


def status() -> BiTStatus:
    """ Checks for the camera status. """
    url = 'bit/status'
    # If the camera is available the request is answered with an empty 200 OK. Otherwise exception is thrown.
    try:
        request('GET', url)
    except YoonikApiException as bit_exception:
        if bit_exception.status_code == 503:
            return BiTStatus.NotAvailable
        raise
    return BiTStatus.Available


def setup():
    """
        Perform BiT setup actions
    """
    url = 'bit/setup'
    request('GET', url)

