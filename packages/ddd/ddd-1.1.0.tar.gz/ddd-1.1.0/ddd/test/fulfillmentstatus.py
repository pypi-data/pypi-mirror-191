# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import enum


class FulfillmentStatus(str, enum.Enum):
    #: We detected that a client created an order for which it may
    #: possible create a fulfillment request.
    detected = 'detected'

    #: The fulfiller unconditionally rejected the request.
    rejected = 'rejected'

    #: The fulfiller accepted the request.
    accepted = 'accepted'