#
# Copyright 2023 by Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Package "web"
"""
API_VERSION = "1.7.1"

from . import transformation
from . import action
from . import notification
from . import sourceconfig
from . import authorization
from . import about
from . import source
from . import registration
from . import toolkit
from . import fault
from . import user
from . import repository
from . import namespace
from . import role
from . import host
from . import storage
from . import connectivity
from . import maskingjob
from . import session
from . import service
from . import policy
from . import job
from . import timeflow
from . import data
from . import permission
from . import snapshot
from . import alert
from . import objects
from . import replication
from . import environment
from . import delphix
from . import jetstream
from . import analytics
from . import system
from . import network
from . import database
from . import timezone
from . import domain
from . import group
from . import capacity
