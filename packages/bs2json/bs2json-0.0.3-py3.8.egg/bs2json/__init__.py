#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .bs2json import BS2Json

# deprecated version compatibility
bs2json = BS2Json
bs2json.convertAll = bs2json.convert_all
bs2json.toJson = bs2json.to_json
