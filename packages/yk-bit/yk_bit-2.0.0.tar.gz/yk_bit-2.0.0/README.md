
![logo](https://yk-website-images.s3.eu-west-1.amazonaws.com/LogoV4_TRANSPARENT.png?)

# Youverse BiometricInThings API: Python SDK & Sample

[![PyPi Version](https://img.shields.io/pypi/v/yk_bit.svg)](https://pypi.org/project/yk-bit/)
[![License](https://img.shields.io/github/license/dev-yoonik/YK-BiT-SDK-Python)](https://github.com/dev-yoonik/YK-BiT-SDK-Python/blob/main/LICENSE)


This repository contains the Python Module of the Youverse BiT API, an offering within [Youverse Services](https://www.youverse.id)

## Getting started

Installing from the source code:

```bash
python setup.py install
```

Use it:

Make sure you have added the environment key-values (YK_BIT_BASE_URL and YK_BIT_X_API_KEY). Machine restart could be required.

```python
from os import getenv
import yk_bit as YKB


# BiometricInThings API Environment Variables
EV_BASE_URL = getenv('YK_BIT_BASE_URL')
EV_API_KEY = getenv('YK_BIT_X_API_KEY')

YKB.BaseUrl.set(EV_BASE_URL)
YKB.Key.set(EV_API_KEY)

# Verifies the camera availability status
if YKB.bit.status() == YKB.BiTStatus.Available:
    
    captured = YKB.capture(capture_timeout=10, anti_spoofing=True, live_quality_analysis=True)
    print(captured)
    
    verified = YKB.verify(reference_image=captured.image, capture_time_out=10, matching_score_threshold=0.8)
    print(verified)
    
    verified_images = YKB.verify_images(probe_image=verified.verified_image, reference_image=captured.image, matching_score_threshold=0.8)
    print(verified_images)


```

 If you're interested in using Youverse BiometricInThings API for identification purposes, please contact us.

## Running the sample

A sample python script is also provided in 'sample' folder.

Run:

```bash
python run_bit_sample.py
```

## Youverse BiT API Details

For a complete specification of our BiT API please check the [swagger file](https://dev-yoonik.github.io/YK-BiT-Documentation/).

## Contact & Support

For more information and trial licenses please [contact us](mailto:tech@youverse.id) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).

