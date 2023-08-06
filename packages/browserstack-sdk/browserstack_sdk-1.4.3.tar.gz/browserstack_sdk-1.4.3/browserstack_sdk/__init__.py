# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack11l_opy_ = 7
def bstack111_opy_ (bstack1l1l_opy_):
    global bstack1l_opy_
    stringNr = ord (bstack1l1l_opy_ [-1])
    bstack1ll1_opy_ = bstack1l1l_opy_ [:-1]
    bstack1ll_opy_ = stringNr % len (bstack1ll1_opy_)
    bstack1l1_opy_ = bstack1ll1_opy_ [:bstack1ll_opy_] + bstack1ll1_opy_ [bstack1ll_opy_:]
    if bstack1lll_opy_:
        bstackl_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack11_opy_ + stringNr) % bstack11l_opy_) for bstack11_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstackl_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack11_opy_ + stringNr) % bstack11l_opy_) for bstack11_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstackl_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l1ll_opy_ = {
	bstack111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭৕"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩ৖"),
  bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩৗ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪ৘"),
  bstack111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ৙"): bstack111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭৚"),
  bstack111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ৛"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫড়"),
  bstack111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪঢ়"): bstack111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧ৞"),
  bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪয়"): bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧৠ"),
  bstack111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧৡ"): bstack111_opy_ (u"ࠪࡲࡦࡳࡥࠨৢ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪৣ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪ৤"),
  bstack111_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ৥"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧ০"),
  bstack111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭১"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭২"),
  bstack111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ৩"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧ৪"),
  bstack111_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ৫"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫ৬"),
  bstack111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭৭"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭৮"),
  bstack111_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ৯"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩৰ"),
  bstack111_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩৱ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ৲"),
  bstack111_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ৳"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ৴"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ৵"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ৶"),
  bstack111_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩ৷"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩ৸"),
  bstack111_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ৹"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ৺"),
  bstack111_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧ৻"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧৼ"),
  bstack111_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫ৽"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫ৾"),
  bstack111_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭৿"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭਀"),
  bstack111_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬਁ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬਂ"),
  bstack111_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩਃ"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ਄"),
  bstack111_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫਅ"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫਆ"),
  bstack111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨਇ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨਈ"),
  bstack111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਉ"): bstack111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨਊ"),
  bstack111_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭਋"): bstack111_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ਌"),
  bstack111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ਍"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ਎"),
  bstack111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ਏ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭ਐ"),
  bstack111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ਑"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ਒"),
  bstack111_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩਓ"): bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬਔ"),
  bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਕ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਖ"),
  bstack111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧਗ"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧਘ"),
  bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਙ"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਚ"),
  bstack111_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ਛ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ਜ"),
}
bstack11111_opy_ = [
  bstack111_opy_ (u"࠭࡯ࡴࠩਝ"),
  bstack111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪਞ"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਟ"),
  bstack111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਠ"),
  bstack111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧਡ"),
  bstack111_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨਢ"),
  bstack111_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬਣ"),
]
bstack1ll1ll_opy_ = {
  bstack111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩਤ"): bstack111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫਥ"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਦ"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫਧ"), bstack111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ਨ")],
  bstack111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ਩"): bstack111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪਪ"),
  bstack111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪਫ"): bstack111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧਬ"),
  bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ਭ"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪਮ"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩਯ")],
  bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬਰ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ਱"),
  bstack111_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪਲ"): bstack111_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬਲ਼"),
  bstack111_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ਴"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩਵ"), bstack111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫਸ਼")],
  bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ਷"): [bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ਸ"), bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭ਹ")]
}
bstack11ll1_opy_ = [
  bstack111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭਺"),
  bstack111_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫ਻"),
  bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ਼"),
  bstack111_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪ਽"),
  bstack111_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ਾ"),
  bstack111_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪਿ"),
  bstack111_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩੀ"),
  bstack111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬੁ"),
  bstack111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ੂ"),
  bstack111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ੃"),
  bstack111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੄"),
  bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ੅"),
]
bstack11ll_opy_ = [
  bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ੆"),
  bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪੇ"),
  bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ੈ"),
  bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੉"),
  bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊"),
  bstack111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬੋ"),
  bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧੌ"),
  bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺ੍ࠩ"),
  bstack111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ੎"),
]
bstack1ll11l_opy_ = [
  bstack111_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬ੏"),
  bstack111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੐"),
  bstack111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬੑ"),
  bstack111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੒"),
  bstack111_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪ੓"),
  bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ੔"),
  bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨ੕"),
  bstack111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ੖"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ੗"),
  bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ੘"),
  bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਖ਼"),
  bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪਗ਼"),
  bstack111_opy_ (u"ࠬࡵࡳࠨਜ਼"),
  bstack111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩੜ"),
  bstack111_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭੝"),
  bstack111_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪਫ਼"),
  bstack111_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩ੟"),
  bstack111_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬ੠"),
  bstack111_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬ੡"),
  bstack111_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩ੢"),
  bstack111_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ੣"),
  bstack111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫ੤"),
  bstack111_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ੥"),
  bstack111_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭੦"),
  bstack111_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫ੧"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ੨"),
  bstack111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ੩"),
  bstack111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ੪"),
  bstack111_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ੫"),
  bstack111_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬ੬"),
  bstack111_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫ੭"),
  bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੮"),
  bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫ੯"),
  bstack111_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫੰ"),
  bstack111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪੱ"),
  bstack111_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧੲ"),
  bstack111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬੳ"),
  bstack111_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪੴ"),
  bstack111_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩੵ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ੶"),
  bstack111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧ੷"),
  bstack111_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨ੸"),
  bstack111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭੹"),
  bstack111_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭੺"),
  bstack111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ੻"),
  bstack111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨ੼"),
  bstack111_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩ੽"),
  bstack111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ੾"),
  bstack111_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ੿"),
  bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩ઀"),
  bstack111_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩઁ"),
  bstack111_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪં"),
  bstack111_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫઃ"),
  bstack111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪ઄"),
  bstack111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪઅ"),
  bstack111_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭આ"),
  bstack111_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩઇ"),
  bstack111_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ઈ"),
  bstack111_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧઉ"),
  bstack111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫઊ"),
  bstack111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫઋ"),
  bstack111_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ઌ"),
  bstack111_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭ઍ"),
  bstack111_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧ઎"),
  bstack111_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧએ"),
  bstack111_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩઐ"),
  bstack111_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫઑ"),
  bstack111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ઒"),
  bstack111_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩઓ"),
  bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬઔ"),
  bstack111_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪક"),
  bstack111_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬખ"),
  bstack111_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩગ"),
  bstack111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫઘ"),
  bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫઙ"),
  bstack111_opy_ (u"ࠬ࡯ࡥࠨચ"),
  bstack111_opy_ (u"࠭ࡥࡥࡩࡨࠫછ"),
  bstack111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧજ"),
  bstack111_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧઝ"),
  bstack111_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫઞ"),
  bstack111_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫટ"),
  bstack111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪઠ"),
  bstack111_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨડ"),
  bstack111_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩઢ"),
  bstack111_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫણ"),
  bstack111_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨત"),
  bstack111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩથ"),
  bstack111_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬદ"),
  bstack111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬધ"),
  bstack111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬન"),
  bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ઩"),
  bstack111_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬપ"),
  bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪફ"),
  bstack111_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭બ"),
  bstack111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧભ"),
  bstack111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧમ"),
  bstack111_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪય"),
  bstack111_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨર"),
  bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ઱")
]
bstack1lll1l_opy_ = {
  bstack111_opy_ (u"ࠨࡸࠪલ"): bstack111_opy_ (u"ࠩࡹࠫળ"),
  bstack111_opy_ (u"ࠪࡪࠬ઴"): bstack111_opy_ (u"ࠫ࡫࠭વ"),
  bstack111_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫશ"): bstack111_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬષ"),
  bstack111_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭સ"): bstack111_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧહ"),
  bstack111_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭઺"): bstack111_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ઻"),
  bstack111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺ઼ࠧ"): bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨઽ"),
  bstack111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩા"): bstack111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪિ"),
  bstack111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫી"): bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬુ"),
  bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ૂ"): bstack111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧૃ"),
  bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ૄ"): bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧૅ"),
  bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨ૆"): bstack111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩે"),
  bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪૈ"): bstack111_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬૉ"),
  bstack111_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭૊"): bstack111_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧો"),
  bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧૌ"): bstack111_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴ્ࠩ"),
  bstack111_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪ૎"): bstack111_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ૏"),
  bstack111_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧૐ"): bstack111_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨ૑"),
  bstack111_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭૒"): bstack111_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ૓"),
  bstack111_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ૔"): bstack111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ૕"),
  bstack111_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ૖"): bstack111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭૗"),
  bstack111_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬ૘"): bstack111_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭૙"),
  bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૚"): bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૛"),
}
bstack1l11ll_opy_ = bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩ૜")
bstack1111l_opy_ = bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬ૝")
bstack1l1l11_opy_ = {
  bstack111_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬ૞"): 50,
  bstack111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ૟"): 40,
  bstack111_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ૠ"): 30,
  bstack111_opy_ (u"࠭ࡩ࡯ࡨࡲࠫૡ"): 20,
  bstack111_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ૢ"): 10
}
DEFAULT_LOG_LEVEL = bstack1l1l11_opy_[bstack111_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ૣ")]
bstack11l1l_opy_ = bstack111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૤")
bstack1lllll_opy_ = bstack111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૥")
bstack11l11_opy_ = bstack111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪ૦")
bstack1ll1l1_opy_ = bstack111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࠫ૧")
bstack1llll1_opy_ = [bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ૨"), bstack111_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ૩")]
bstack11l1_opy_ = [bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ૪"), bstack111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ૫")]
bstack1ll1l_opy_ = [
  bstack111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫ૬"),
  bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૭"),
  bstack111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ૮"),
  bstack111_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪ૯"),
  bstack111_opy_ (u"ࠧࡢࡲࡳࠫ૰"),
  bstack111_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭૱"),
  bstack111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ૲"),
  bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪ૳"),
  bstack111_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩ૴"),
  bstack111_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪ૵"),
  bstack111_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧ૶"), bstack111_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪ૷"),
  bstack111_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫ૸"),
  bstack111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨૹ"),
  bstack111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧૺ"),
  bstack111_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧૻ"),
  bstack111_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭ૼ"),
  bstack111_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫ૽"), bstack111_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫ૾"), bstack111_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ૿"), bstack111_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪ଀"), bstack111_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬଁ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩଂ"),
  bstack111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩଃ"),
  bstack111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨ଄"), bstack111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫଅ"),
  bstack111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ଆ"),
  bstack111_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪଇ"),
  bstack111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩଈ"),
  bstack111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬଉ"),
  bstack111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪଊ"),
  bstack111_opy_ (u"࠭ࡡࡷࡦࠪଋ"), bstack111_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪଌ"), bstack111_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ଍"), bstack111_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪ଎"),
  bstack111_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨଏ"), bstack111_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪଐ"), bstack111_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨ଑"),
  bstack111_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨ଒"), bstack111_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬଓ"),
  bstack111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪଔ"), bstack111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬକ"), bstack111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨଖ"), bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ଗ"), bstack111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩଘ"),
  bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩଙ"), bstack111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫଚ"),
  bstack111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪଛ"),
  bstack111_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧଜ"),
  bstack111_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩଝ"), bstack111_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬଞ"), bstack111_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪଟ"), bstack111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩଠ"),
  bstack111_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬଡ"),
  bstack111_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪଢ"), bstack111_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩଣ"),
  bstack111_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪତ"),
  bstack111_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭ଥ"),
  bstack111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧଦ"),
  bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ଧ"),
  bstack111_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨନ"),
  bstack111_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ଩"),
  bstack111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪପ"),
  bstack111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩଫ"),
  bstack111_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨବ"),
  bstack111_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩଭ"),
  bstack111_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧମ"),
  bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ଯ"),
  bstack111_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬର"),
  bstack111_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩ଱"),
  bstack111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨଲ"),
  bstack111_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨଳ"),
  bstack111_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬ଴"),
  bstack111_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪଵ"), bstack111_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫଶ"), bstack111_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫଷ"),
  bstack111_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ସ"),
  bstack111_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧହ"),
  bstack111_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭଺"),
  bstack111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧ଻"),
  bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰ଼ࠪ"),
  bstack111_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫଽ"),
  bstack111_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫା"), bstack111_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨି"), bstack111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ୀ"),
  bstack111_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫୁ"),
  bstack111_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ୂ"),
  bstack111_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨୃ"),
  bstack111_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧୄ"),
  bstack111_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫ୅"), bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨ୆"),
  bstack111_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭େ"), bstack111_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨୈ"),
  bstack111_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬ୉"),
  bstack111_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬ୊"),
  bstack111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪୋ"), bstack111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬୌ"), bstack111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬୍࠭"), bstack111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪ୎"),
  bstack111_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫ୏"),
  bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭୐"),
  bstack111_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩ୑"),
  bstack111_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧ୒"),
  bstack111_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬ୓"),
  bstack111_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫ୔"),
  bstack111_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ୕"), bstack111_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬୖ"),
  bstack111_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨୗ"),
  bstack111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭୘"),
  bstack111_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨ୙"),
  bstack111_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨ୚"),
  bstack111_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫ୛"),
  bstack111_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭ଡ଼"),
  bstack111_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬଢ଼"),
  bstack111_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭୞"),
  bstack111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ୟ"),
  bstack111_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬୠ"),
  bstack111_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ୡ"),
  bstack111_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨୢ"),
  bstack111_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩୣ"),
  bstack111_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭୤"),
  bstack111_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧ୥"),
  bstack111_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩ୦"),
  bstack111_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨ୧"),
  bstack111_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩ୨"),
  bstack111_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭୩"),
  bstack111_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩ୪"),
  bstack111_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧ୫"),
  bstack111_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨ୬"), bstack111_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭୭"),
  bstack111_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫ୮"), bstack111_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩ୯"),
  bstack111_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧ୰"),
  bstack111_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ୱ"),
  bstack111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭୲"),
  bstack111_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩ୳"), bstack111_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩ୴"),
  bstack111_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪ୵"),
  bstack111_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭୶"),
  bstack111_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩ୷"),
  bstack111_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫ୸"),
  bstack111_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭୹"),
  bstack111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨ୺"),
  bstack111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫ୻"),
  bstack111_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭୼"),
  bstack111_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪ୽"),
  bstack111_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨ୾"), bstack111_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧ୿"),
  bstack111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫ஀")
]
bstack1lll1_opy_ = bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡺࡶ࡬ࡰࡣࡧࠫ஁")
bstack1l1l1_opy_ = [bstack111_opy_ (u"࠭࠮ࡢࡲ࡮ࠫஂ"), bstack111_opy_ (u"ࠧ࠯ࡣࡤࡦࠬஃ"), bstack111_opy_ (u"ࠨ࠰࡬ࡴࡦ࠭஄")]
bstack1l111_opy_ = [bstack111_opy_ (u"ࠩ࡬ࡨࠬஅ"), bstack111_opy_ (u"ࠪࡴࡦࡺࡨࠨஆ"), bstack111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧஇ"), bstack111_opy_ (u"ࠬࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࠫஈ")]
bstack1l1ll1_opy_ = {
  bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭உ"): bstack111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬஊ"),
  bstack111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஋"): bstack111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ஌"),
  bstack111_opy_ (u"ࠪࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ஍"): bstack111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬஎ"),
  bstack111_opy_ (u"ࠬ࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨஏ"): bstack111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬஐ"),
  bstack111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡶ࡬ࡳࡳࡹࠧ஑"): bstack111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩஒ")
}
bstack111l_opy_ = [
  bstack111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧஓ"),
  bstack111_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨஔ"),
  bstack111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬக"),
  bstack111_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ஖"),
  bstack111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ஗"),
]
bstack1l11_opy_ = bstack11ll_opy_ + bstack1ll11l_opy_ + bstack1ll1l_opy_
bstack1l1l1l_opy_ = [
  bstack111_opy_ (u"ࠧ࡟࡮ࡲࡧࡦࡲࡨࡰࡵࡷࠨࠬ஘"),
  bstack111_opy_ (u"ࠨࡠࡥࡷ࠲ࡲ࡯ࡤࡣ࡯࠲ࡨࡵ࡭ࠥࠩங"),
  bstack111_opy_ (u"ࠩࡡ࠵࠷࠽࠮ࠨச"),
  bstack111_opy_ (u"ࠪࡢ࠶࠶࠮ࠨ஛"),
  bstack111_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠴࡟࠻࠳࠹࡞࠰ࠪஜ"),
  bstack111_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠶ࡠ࠶࠭࠺࡟࠱ࠫ஝"),
  bstack111_opy_ (u"࠭࡞࠲࠹࠵࠲࠸ࡡ࠰࠮࠳ࡠ࠲ࠬஞ"),
  bstack111_opy_ (u"ࠧ࡟࠳࠼࠶࠳࠷࠶࠹࠰ࠪட")
]
bstack1llll_opy_ = bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁࠬ஠")
bstack11lll_opy_ = bstack111_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡨࡺࡪࡴࡴࠨ஡")
bstack1l1lll_opy_ = [ bstack111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ஢") ]
bstack1ll111_opy_ = [ bstack111_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪண") ]
bstack1ll11_opy_ = [ bstack111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬத") ]
bstack111ll_opy_ = bstack111_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨ஥")
bstack1lll11_opy_ = bstack111_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪ஦")
bstack1l11l_opy_ = bstack111_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬ஧")
bstack111l1_opy_ = bstack111_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨந")
bstack11l111ll_opy_ = bstack111_opy_ (u"ࠪࡗࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠯ࠤࡺࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡀࠠࡼࡿࠪன")
bstack11l1l11l_opy_ = bstack111_opy_ (u"ࠫࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡴࡧࡷࡹࡵࠧࠧப")
bstack11l1l111_opy_ = bstack111_opy_ (u"ࠬࡖࡡࡳࡵࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧ஫")
bstack11l1llll_opy_ = bstack111_opy_ (u"࠭ࡓࡢࡰ࡬ࡸ࡮ࢀࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ஬")
bstack1llll11l_opy_ = bstack111_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡨࡶࡤࠣࡹࡷࡲ࠺ࠡࡽࢀࠫ஭")
bstack1ll1l1lll_opy_ = bstack111_opy_ (u"ࠨࡕࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥࢁࡽࠨம")
bstack111lllll_opy_ = bstack111_opy_ (u"ࠩࡕࡩࡨ࡫ࡩࡷࡧࡧࠤ࡮ࡴࡴࡦࡴࡵࡹࡵࡺࠬࠡࡧࡻ࡭ࡹ࡯࡮ࡨࠩய")
bstack1llll11ll_opy_ = bstack111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨர")
bstack1llllllll_opy_ = bstack111_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩற")
bstack1ll1ll1l_opy_ = bstack111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࠱ࠦࡰࡢࡤࡲࡸࠥࡧ࡮ࡥࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࠤࡵࡧࡣ࡬ࡣࡪࡩࡸࠦࡴࡰࠢࡵࡹࡳࠦࡲࡰࡤࡲࡸࠥࡺࡥࡴࡶࡶࠤ࡮ࡴࠠࡱࡣࡵࡥࡱࡲࡥ࡭࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡵࡧࡢࡰࡶࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡲࡩࡣࡴࡤࡶࡾࡦࠧல")
bstack11l111l1_opy_ = bstack111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡢࡦࡪࡤࡺࡪࡦࠧள")
bstack1l1lll1l_opy_ = bstack111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡣࡳࡴ࡮ࡻ࡭࠮ࡥ࡯࡭ࡪࡴࡴࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡂࡲࡳ࡭ࡺࡳ࠭ࡑࡻࡷ࡬ࡴࡴ࠭ࡄ࡮࡬ࡩࡳࡺࡠࠨழ")
bstack1lll1l11_opy_ = bstack111_opy_ (u"ࠨࡊࡤࡲࡩࡲࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡲ࡯ࡴࡧࠪவ")
bstack1ll1ll1l1_opy_ = bstack111_opy_ (u"ࠩࡄࡰࡱࠦࡤࡰࡰࡨࠥࠬஶ")
bstack11ll1ll_opy_ = bstack111_opy_ (u"ࠪࡇࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࠢࡤࡸࠥࠨࡻࡾࠤ࠱ࠤࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨஷ")
bstack1l111l11_opy_ = bstack111_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡷ࡫ࡤࡦࡰࡷ࡭ࡦࡲࡳࠡࡰࡲࡸࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡣࡧࡨࠥࡺࡨࡦ࡯ࠣ࡭ࡳࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡢࡵࠣࠦࡺࡹࡥࡳࡐࡤࡱࡪࠨࠠࡢࡰࡧࠤࠧࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠣࠢࡲࡶࠥࡹࡥࡵࠢࡷ࡬ࡪࡳࠠࡢࡵࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶ࠾ࠥࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢࠡࡣࡱࡨࠥࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠤࠪஸ")
bstack11lllll1_opy_ = bstack111_opy_ (u"ࠬࡓࡡ࡭ࡨࡲࡶࡲ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠢࡼࡿࠥࠫஹ")
bstack1ll1l1l11_opy_ = bstack111_opy_ (u"࠭ࡅ࡯ࡥࡲࡹࡳࡺࡥࡳࡧࡧࠤࡪࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦ࠭ࠡࡽࢀࠫ஺")
bstack1ll1llll_opy_ = bstack111_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧ஻")
bstack111l1ll1_opy_ = bstack111_opy_ (u"ࠨࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠨ஼")
bstack1111lll1_opy_ = bstack111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠠࡪࡵࠣࡲࡴࡽࠠࡳࡷࡱࡲ࡮ࡴࡧࠢࠩ஽")
bstack1llll1ll1_opy_ = bstack111_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡳࡵࡣࡵࡸࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮࠽ࠤࢀࢃࠧா")
bstack1l1ll1ll1_opy_ = bstack111_opy_ (u"ࠫࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦ࡬ࡰࡥࡤࡰࠥࡨࡩ࡯ࡣࡵࡽࠥࡽࡩࡵࡪࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࢁࡽࠨி")
bstack11l11111_opy_ = bstack111_opy_ (u"࡛ࠬࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂ࠭ீ")
bstack111lll1l_opy_ = bstack111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠬு")
bstack1l1l1l1l_opy_ = bstack111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࠡࡣࡱࠤࡦࡶࡰࡳࡱࡳࡶ࡮ࡧࡴࡦࠢࡉ࡛ࠥ࠮ࡲࡰࡤࡲࡸ࠴ࡶࡡࡣࡱࡷ࠭ࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪ࠲ࠠࡴ࡭࡬ࡴࠥࡺࡨࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡱࡥࡺࠢ࡬ࡲࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡶ࡭ࡲࡶ࡬ࡦࠢࡳࡽࡹ࡮࡯࡯ࠢࡶࡧࡷ࡯ࡰࡵࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡥࡳࡿࠠࡇ࡙࠱ࠫூ")
bstack111llll_opy_ = bstack111_opy_ (u"ࠨࡕࡨࡸࡹ࡯࡮ࡨࠢ࡫ࡸࡹࡶࡐࡳࡱࡻࡽ࠴࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡵ࡮ࠡࡥࡸࡶࡷ࡫࡮ࡵ࡮ࡼࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡱࡩࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࠨࡼࡿࠬ࠰ࠥࡶ࡬ࡦࡣࡶࡩࠥࡻࡰࡨࡴࡤࡨࡪࠦࡴࡰࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡂࡂ࠺࠮࠱࠰࠳ࠤࡴࡸࠠࡳࡧࡩࡩࡷࠦࡴࡰࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡲࡥ࡯࡫ࡸࡱ࠴ࡸࡵ࡯࠯ࡷࡩࡸࡺࡳ࠮ࡤࡨ࡬࡮ࡴࡤ࠮ࡲࡵࡳࡽࡿࠣࡱࡻࡷ࡬ࡴࡴࠠࡧࡱࡵࠤࡦࠦࡷࡰࡴ࡮ࡥࡷࡵࡵ࡯ࡦ࠱ࠫ௃")
bstack111l111l_opy_ = bstack111_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡿ࡭࡭ࠢࡩ࡭ࡱ࡫࠮࠯ࠩ௄")
bstack1llllll1_opy_ = bstack111_opy_ (u"ࠪࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡺࡨࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩ࡭ࡱ࡫ࠡࠨ௅")
bstack11l1lll_opy_ = bstack111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧ࠱ࠤࢀࢃࠧெ")
bstack11l1ll1l_opy_ = bstack111_opy_ (u"ࠬࡋࡸࡱࡧࡦࡸࡪࡪࠠࡢࡶࠣࡰࡪࡧࡳࡵࠢ࠴ࠤ࡮ࡴࡰࡶࡶ࠯ࠤࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦ࠰ࠨே")
bstack11l1ll1_opy_ = bstack111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡇࡰࡱࠢࡸࡴࡱࡵࡡࡥ࠰ࠣࡿࢂ࠭ை")
bstack111111l_opy_ = bstack111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡲ࡯ࡢࡦࠣࡅࡵࡶ࠮ࠡࡋࡱࡺࡦࡲࡩࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡼࡿ࠱ࠫ௉")
bstack1ll11lll1_opy_ = bstack111_opy_ (u"ࠨࡍࡨࡽࡸࠦࡣࡢࡰࡱࡳࡹࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡣࡶࠤࡦࡶࡰࠡࡸࡤࡰࡺ࡫ࡳ࠭ࠢࡸࡷࡪࠦࡡ࡯ࡻࠣࡳࡳ࡫ࠠࡱࡴࡲࡴࡪࡸࡴࡺࠢࡩࡶࡴࡳࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠱ࠦ࡯࡯࡮ࡼࠤࠧࡶࡡࡵࡪࠥࠤࡦࡴࡤࠡࠤࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠧࠦࡣࡢࡰࠣࡧࡴ࠳ࡥࡹ࡫ࡶࡸࠥࡺ࡯ࡨࡧࡷ࡬ࡪࡸ࠮ࠨொ")
bstack1l1l111l_opy_ = bstack111_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠤࡦࡸࡥࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠴ࠠࡇࡱࡵࠤࡲࡵࡲࡦࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡴࡱ࡫ࡡࡴࡧࠣࡺ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲࡳ࡭ࡺࡳ࠯ࡴࡧࡷ࠱ࡺࡶ࠭ࡵࡧࡶࡸࡸ࠵ࡳࡱࡧࡦ࡭࡫ࡿ࠭ࡢࡲࡳࠫோ")
bstack11ll111_opy_ = bstack111_opy_ (u"ࠪ࡟ࡎࡴࡶࡢ࡮࡬ࡨࠥࡧࡰࡱࠢࡳࡶࡴࡶࡥࡳࡶࡼࡡ࡙ࠥࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࡳࠡࡱࡩࠤࡦࡶࡰࠡࡣࡵࡩࠥࡵࡦࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠴ࠠࡇࡱࡵࠤࡲࡵࡲࡦࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡴࡱ࡫ࡡࡴࡧࠣࡺ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡨࡴࡩࡳ࠰ࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲࡳ࡭ࡺࡳ࠯ࡴࡧࡷ࠱ࡺࡶ࠭ࡵࡧࡶࡸࡸ࠵ࡳࡱࡧࡦ࡭࡫ࡿ࠭ࡢࡲࡳࠫௌ")
bstack1ll1ll111_opy_ = bstack111_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡧࡰࡱࠢ࡬ࡨࠥࢁࡽࠡࡨࡲࡶࠥ࡮ࡡࡴࡪࠣ࠾ࠥࢁࡽ࠯்ࠩ")
bstack11111l1_opy_ = bstack111_opy_ (u"ࠬࡇࡰࡱࠢࡘࡴࡱࡵࡡࡥࡧࡧࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠤࡎࡊࠠ࠻ࠢࡾࢁࠬ௎")
bstack1llll1ll_opy_ = bstack111_opy_ (u"࠭ࡕࡴ࡫ࡱ࡫ࠥࡇࡰࡱࠢ࠽ࠤࢀࢃ࠮ࠨ௏")
bstack1ll1ll11l_opy_ = bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࡹࠬࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮ࠠࡱࡣࡵࡥࡱࡲࡥ࡭ࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦ࠽ࠡ࠳ࠪௐ")
bstack1lll111l_opy_ = bstack111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠺ࠡࡽࢀࠫ௑")
bstack1ll11ll_opy_ = bstack111_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡩ࡬ࡰࡵࡨࠤࡧࡸ࡯ࡸࡵࡨࡶ࠿ࠦࡻࡾࠩ௒")
bstack1l1l11l1_opy_ = bstack111_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡶࡪࡧࡳࡰࡰࠣࡪࡴࡸࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡧࡤࡸࡺࡸࡥࠡࡨࡤ࡭ࡱࡻࡲࡦ࠰ࠣࡿࢂ࠭௓")
bstack1ll1lll11_opy_ = bstack111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡥࡵ࡯ࠠࡤࡣ࡯ࡰ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ௔")
bstack1l1ll111_opy_ = bstack111_opy_ (u"࡛ࠬ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵ࡫ࡳࡼࠦࡢࡶ࡫࡯ࡨ࡛ࠥࡒࡍ࠮ࠣࡥࡸࠦࡢࡶ࡫࡯ࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡸࡷࡪࡪ࠮ࠨ௕")
bstack111l11ll_opy_ = bstack111_opy_ (u"࠭ࡓࡦࡴࡹࡩࡷࠦࡳࡪࡦࡨࠤࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠨࡼࡿࠬࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡸࡧ࡭ࡦࠢࡤࡷࠥࡩ࡬ࡪࡧࡱࡸࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠪ௖")
bstack11111l_opy_ = bstack111_opy_ (u"ࠧࡗ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡴࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡤࡢࡵ࡫ࡦࡴࡧࡲࡥ࠼ࠣࡿࢂ࠭ௗ")
bstack1lll11l1_opy_ = bstack111_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡦࡩࡣࡦࡵࡶࠤࡦࠦࡰࡳ࡫ࡹࡥࡹ࡫ࠠࡥࡱࡰࡥ࡮ࡴ࠺ࠡࡽࢀࠤ࠳ࠦࡓࡦࡶࠣࡸ࡭࡫ࠠࡧࡱ࡯ࡰࡴࡽࡩ࡯ࡩࠣࡧࡴࡴࡦࡪࡩࠣ࡭ࡳࠦࡹࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡧ࡫࡯ࡩ࠿ࠦ࡜࡯࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱࠲ࠦ࡜࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡀࠠࡵࡴࡸࡩࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠬ௘")
bstack1l11lll_opy_ = bstack111_opy_ (u"ࠩࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱࡥࡥࡳࡴࡲࡶࠥࡀࠠࡼࡿࠪ௙")
bstack1lllll1l1_opy_ = bstack111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡙ࡥࡵࡷࡳࠤࢀࢃࠢ௚")
bstack11l1l11_opy_ = bstack111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡅࡹࡺࡥ࡮ࡲࡷࡩࡩࠦࡻࡾࠤ௛")
bstack1l11l1_opy_ = bstack111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡱࡨࡤࡧ࡭ࡱ࡮࡬ࡸࡺࡪࡥࡠࡧࡹࡩࡳࡺࠠࡧࡱࡵࠤࡘࡊࡋࡕࡧࡶࡸࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠡࡽࢀࠦ௜")
bstack111111_opy_ = bstack111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨ࡬ࡶࡪࡥࡲࡦࡳࡸࡩࡸࡺࠠࡼࡿࠥ௝")
bstack11l11l11_opy_ = bstack111_opy_ (u"ࠢࡑࡑࡖࡘࠥࡋࡶࡦࡰࡷࠤࢀࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢ࠽ࠤࢀࢃࠢ௞")
bstack1l1l1l11_opy_ = bstack111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠࡱࡴࡲࡼࡾࠦࡳࡦࡶࡷ࡭ࡳ࡭ࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ௟")
from ._version import __version__
bstack11111ll1_opy_ = None
CONFIG = {}
bstack1ll1ll1_opy_ = None
bstack1ll1lll1l_opy_ = None
bstack11l1111l_opy_ = None
bstack111ll11l_opy_ = -1
bstack1lll11ll1_opy_ = DEFAULT_LOG_LEVEL
bstack111ll1l_opy_ = 1
bstack1lll1l1l1_opy_ = False
bstack1ll1111l1_opy_ = bstack111_opy_ (u"ࠩࠪ௠")
bstack1l1l11ll_opy_ = bstack111_opy_ (u"ࠪࠫ௡")
bstack1ll11l1_opy_ = False
bstack1ll11l1l_opy_ = True
bstack1llll111l_opy_ = None
bstack1lllll11l_opy_ = None
bstack1ll111ll_opy_ = None
bstack111l1l11_opy_ = None
bstack1l1ll1ll_opy_ = None
bstack1lllll11_opy_ = None
bstack11ll1ll1_opy_ = None
bstack1ll11l11l_opy_ = None
bstack1l1111l1_opy_ = None
bstack1111llll_opy_ = None
bstack1l11ll1l_opy_ = None
bstack11l1lll1_opy_ = bstack111_opy_ (u"ࠦࠧ௢")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lll11ll1_opy_,
                    format=bstack111_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪ௣"),
                    datefmt=bstack111_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௤"))
def bstack1llll1111_opy_():
  global CONFIG
  global bstack1lll11ll1_opy_
  if bstack111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ௥") in CONFIG:
    bstack1lll11ll1_opy_ = bstack1l1l11_opy_[CONFIG[bstack111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ௦")]]
    logging.getLogger().setLevel(bstack1lll11ll1_opy_)
def bstack1llll1l1l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1llllll1l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡤࡱࡱࡪ࡮࡭ࡦࡪ࡮ࡨࠦ௧") in args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1llll111l_opy_
      bstack1llll111l_opy_ = path
      return path
  return None
def bstack1l1l11l_opy_():
  bstack1ll111l_opy_ = bstack1llllll1l_opy_()
  if bstack1ll111l_opy_ and os.path.exists(os.path.abspath(bstack1ll111l_opy_)):
    fileName = bstack1ll111l_opy_
  if bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧ௨") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ௩")])) and not bstack111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧ௪") in locals():
    fileName = os.environ[bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ௫")]
  if not bstack111_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩ௬") in locals():
    fileName = bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ௭")
  bstack1l11llll_opy_ = os.path.abspath(fileName)
  if not os.path.exists(bstack1l11llll_opy_):
    fileName = bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭௮")
    bstack1l11llll_opy_ = os.path.abspath(fileName)
    if not os.path.exists(bstack1l11llll_opy_):
      bstack1ll1llll1_opy_(
        bstack11ll1ll_opy_.format(os.getcwd()))
  with open(bstack1l11llll_opy_, bstack111_opy_ (u"ࠪࡶࠬ௯")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1ll1llll1_opy_(bstack11lllll1_opy_.format(str(exc)))
def bstack1l111ll1_opy_(config):
  bstack11lll1l_opy_ = bstack1ll1lll1_opy_(config)
  for option in list(bstack11lll1l_opy_):
    if option.lower() in bstack1lll1l_opy_ and option != bstack1lll1l_opy_[option.lower()]:
      bstack11lll1l_opy_[bstack1lll1l_opy_[option.lower()]] = bstack11lll1l_opy_[option]
      del bstack11lll1l_opy_[option]
  return config
def bstack11111ll_opy_(config):
  bstack1llllll_opy_ = config.keys()
  for bstack1lll11l11_opy_, bstack111111l1_opy_ in bstack1l1ll_opy_.items():
    if bstack111111l1_opy_ in bstack1llllll_opy_:
      config[bstack1lll11l11_opy_] = config[bstack111111l1_opy_]
      del config[bstack111111l1_opy_]
  for bstack1lll11l11_opy_, bstack111111l1_opy_ in bstack1ll1ll_opy_.items():
    if isinstance(bstack111111l1_opy_, list):
      for bstack11l11lll_opy_ in bstack111111l1_opy_:
        if bstack11l11lll_opy_ in bstack1llllll_opy_:
          config[bstack1lll11l11_opy_] = config[bstack11l11lll_opy_]
          del config[bstack11l11lll_opy_]
          break
    elif bstack111111l1_opy_ in bstack1llllll_opy_:
        config[bstack1lll11l11_opy_] = config[bstack111111l1_opy_]
        del config[bstack111111l1_opy_]
  for bstack11l11lll_opy_ in list(config):
    for bstack111l1ll_opy_ in bstack1l11_opy_:
      if bstack11l11lll_opy_.lower() == bstack111l1ll_opy_.lower() and bstack11l11lll_opy_ != bstack111l1ll_opy_:
        config[bstack111l1ll_opy_] = config[bstack11l11lll_opy_]
        del config[bstack11l11lll_opy_]
  bstack1l1llll11_opy_ = []
  if bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௰") in config:
    bstack1l1llll11_opy_ = config[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௱")]
  for platform in bstack1l1llll11_opy_:
    for bstack11l11lll_opy_ in list(platform):
      for bstack111l1ll_opy_ in bstack1l11_opy_:
        if bstack11l11lll_opy_.lower() == bstack111l1ll_opy_.lower() and bstack11l11lll_opy_ != bstack111l1ll_opy_:
          platform[bstack111l1ll_opy_] = platform[bstack11l11lll_opy_]
          del platform[bstack11l11lll_opy_]
  for bstack1lll11l11_opy_, bstack111111l1_opy_ in bstack1ll1ll_opy_.items():
    for platform in bstack1l1llll11_opy_:
      if isinstance(bstack111111l1_opy_, list):
        for bstack11l11lll_opy_ in bstack111111l1_opy_:
          if bstack11l11lll_opy_ in platform:
            platform[bstack1lll11l11_opy_] = platform[bstack11l11lll_opy_]
            del platform[bstack11l11lll_opy_]
            break
      elif bstack111111l1_opy_ in platform:
        platform[bstack1lll11l11_opy_] = platform[bstack111111l1_opy_]
        del platform[bstack111111l1_opy_]
  for bstack1l1111ll_opy_ in bstack1l1ll1_opy_:
    if bstack1l1111ll_opy_ in config:
      if not bstack1l1ll1_opy_[bstack1l1111ll_opy_] in config:
        config[bstack1l1ll1_opy_[bstack1l1111ll_opy_]] = {}
      config[bstack1l1ll1_opy_[bstack1l1111ll_opy_]].update(config[bstack1l1111ll_opy_])
      del config[bstack1l1111ll_opy_]
  for platform in bstack1l1llll11_opy_:
    for bstack1l1111ll_opy_ in bstack1l1ll1_opy_:
      if bstack1l1111ll_opy_ in list(platform):
        if not bstack1l1ll1_opy_[bstack1l1111ll_opy_] in platform:
          platform[bstack1l1ll1_opy_[bstack1l1111ll_opy_]] = {}
        platform[bstack1l1ll1_opy_[bstack1l1111ll_opy_]].update(platform[bstack1l1111ll_opy_])
        del platform[bstack1l1111ll_opy_]
  config = bstack1l111ll1_opy_(config)
  return config
def bstack111l1l1l_opy_(config):
  global bstack1l1l11ll_opy_
  if bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௲") in config and str(config[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௳")]).lower() != bstack111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௴"):
    if not bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௵") in config:
      config[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ௶")] = {}
    if not bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௷") in config[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௸")]:
      if bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ௹") in os.environ:
        config[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ௺")][bstack111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௻")] = os.environ[bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ௼")]
      else:
        current_time = datetime.datetime.now()
        bstack1ll11l11_opy_ = current_time.strftime(bstack111_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧ௽"))
        hostname = socket.gethostname()
        bstack11lll111_opy_ = bstack111_opy_ (u"ࠫࠬ௾").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack111_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧ௿").format(bstack1ll11l11_opy_, hostname, bstack11lll111_opy_)
        config[bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪఀ")][bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఁ")] = identifier
    bstack1l1l11ll_opy_ = config[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬం")][bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫః")]
  return config
def bstack1l1llllll_opy_(config):
  if bstack111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ఄ") in config and config[bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧఅ")] not in bstack11l1_opy_:
    return config[bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨఆ")]
  elif bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩఇ") in os.environ:
    return os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪఈ")]
  else:
    return None
def bstack1l1lll1l1_opy_(config):
  if bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫఉ") in os.environ:
    return os.environ[bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬఊ")]
  elif bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ఋ") in config:
    return config[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧఌ")]
  else:
    return None
def bstack1l1lll1_opy_():
  if (
    isinstance(os.getenv(bstack111_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪ఍")), str) and len(os.getenv(bstack111_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫఎ"))) > 0
  ) or (
    isinstance(os.getenv(bstack111_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭ఏ")), str) and len(os.getenv(bstack111_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧఐ"))) > 0
  ):
    return os.getenv(bstack111_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨ఑"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠪࡇࡎ࠭ఒ"))).lower() == bstack111_opy_ (u"ࠫࡹࡸࡵࡦࠩఓ") and str(os.getenv(bstack111_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡈࡏࠧఔ"))).lower() == bstack111_opy_ (u"࠭ࡴࡳࡷࡨࠫక"):
    return os.getenv(bstack111_opy_ (u"ࠧࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠪఖ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠨࡅࡌࠫగ"))).lower() == bstack111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧఘ") and str(os.getenv(bstack111_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࠪఙ"))).lower() == bstack111_opy_ (u"ࠫࡹࡸࡵࡦࠩచ"):
    return os.getenv(bstack111_opy_ (u"࡚ࠬࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫఛ"), 0)
  if str(os.getenv(bstack111_opy_ (u"࠭ࡃࡊࠩజ"))).lower() == bstack111_opy_ (u"ࠧࡵࡴࡸࡩࠬఝ") and str(os.getenv(bstack111_opy_ (u"ࠨࡅࡌࡣࡓࡇࡍࡆࠩఞ"))).lower() == bstack111_opy_ (u"ࠩࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠫట"):
    return 0 # bstack1ll11ll1l_opy_ bstack1ll1111l_opy_ not set build number env
  if os.getenv(bstack111_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍ࠭ఠ")) and os.getenv(bstack111_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠧడ")):
    return os.getenv(bstack111_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧఢ"), 0)
  if str(os.getenv(bstack111_opy_ (u"࠭ࡃࡊࠩణ"))).lower() == bstack111_opy_ (u"ࠧࡵࡴࡸࡩࠬత") and str(os.getenv(bstack111_opy_ (u"ࠨࡆࡕࡓࡓࡋࠧథ"))).lower() == bstack111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧద"):
    return os.getenv(bstack111_opy_ (u"ࠪࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨధ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠫࡈࡏࠧన"))).lower() == bstack111_opy_ (u"ࠬࡺࡲࡶࡧࠪ఩") and str(os.getenv(bstack111_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࠩప"))).lower() == bstack111_opy_ (u"ࠧࡵࡴࡸࡩࠬఫ"):
    return os.getenv(bstack111_opy_ (u"ࠨࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠫబ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠩࡆࡍࠬభ"))).lower() == bstack111_opy_ (u"ࠪࡸࡷࡻࡥࠨమ") and str(os.getenv(bstack111_opy_ (u"ࠫࡌࡏࡔࡍࡃࡅࡣࡈࡏࠧయ"))).lower() == bstack111_opy_ (u"ࠬࡺࡲࡶࡧࠪర"):
    return os.getenv(bstack111_opy_ (u"࠭ࡃࡊࡡࡍࡓࡇࡥࡉࡅࠩఱ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠧࡄࡋࠪల"))).lower() == bstack111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ళ") and str(os.getenv(bstack111_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠬఴ"))).lower() == bstack111_opy_ (u"ࠪࡸࡷࡻࡥࠨవ"):
    return os.getenv(bstack111_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭శ"), 0)
  if str(os.getenv(bstack111_opy_ (u"࡚ࠬࡆࡠࡄࡘࡍࡑࡊࠧష"))).lower() == bstack111_opy_ (u"࠭ࡴࡳࡷࡨࠫస"):
    return os.getenv(bstack111_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧహ"), 0)
  return -1
def bstack11l1111_opy_(bstack1llll1l11_opy_):
  global CONFIG
  if not bstack111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ఺") in CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ఻")]:
    return
  CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ఼ࠬ")] = CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ఽ")].replace(
    bstack111_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧా"),
    str(bstack1llll1l11_opy_)
  )
def bstack1lll1lll_opy_():
  global CONFIG
  if not bstack111_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬి") in CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩీ")]:
    return
  current_time = datetime.datetime.now()
  bstack1ll11l11_opy_ = current_time.strftime(bstack111_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭ు"))
  CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫూ")] = CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬృ")].replace(
    bstack111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪౄ"),
    bstack1ll11l11_opy_
  )
def bstack11l1ll11_opy_():
  global CONFIG
  if bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ౅") in CONFIG and not bool(CONFIG[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨె")]):
    del CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩే")]
    return
  if not bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪై") in CONFIG:
    CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ౉")] = bstack111_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ొ")
  if bstack111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪో") in CONFIG[bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧౌ")]:
    bstack1lll1lll_opy_()
    os.environ[bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆ్ࠪ")] = CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ౎")]
  if not bstack111_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ౏") in CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ౐")]:
    return
  bstack1llll1l11_opy_ = bstack111_opy_ (u"ࠪࠫ౑")
  bstack1llll1lll_opy_ = bstack1l1lll1_opy_()
  if bstack1llll1lll_opy_ != -1:
    bstack1llll1l11_opy_ = bstack111_opy_ (u"ࠫࡈࡏࠠࠨ౒") + str(bstack1llll1lll_opy_)
  if bstack1llll1l11_opy_ == bstack111_opy_ (u"ࠬ࠭౓"):
    bstack1lll1l1l_opy_ = bstack1l11ll11_opy_(CONFIG[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ౔")])
    if bstack1lll1l1l_opy_ != -1:
      bstack1llll1l11_opy_ = str(bstack1lll1l1l_opy_)
  if bstack1llll1l11_opy_:
    bstack11l1111_opy_(bstack1llll1l11_opy_)
    os.environ[bstack111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇౕࠫ")] = CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴౖࠪ")]
def bstack11111l1l_opy_(bstack1111ll11_opy_, bstack1lll1111l_opy_, path):
  bstack1ll1l11ll_opy_ = {
    bstack111_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭౗"): bstack1lll1111l_opy_
  }
  if os.path.exists(path):
    bstack11llll1l_opy_ = json.load(open(path, bstack111_opy_ (u"ࠪࡶࡧ࠭ౘ")))
  else:
    bstack11llll1l_opy_ = {}
  bstack11llll1l_opy_[bstack1111ll11_opy_] = bstack1ll1l11ll_opy_
  with open(path, bstack111_opy_ (u"ࠦࡼ࠱ࠢౙ")) as outfile:
    json.dump(bstack11llll1l_opy_, outfile)
def bstack1l11ll11_opy_(bstack1111ll11_opy_):
  bstack1111ll11_opy_ = str(bstack1111ll11_opy_)
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠬࢄࠧౚ")), bstack111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭౛"))
  try:
    if not os.path.exists(bstack111ll11_opy_):
      os.makedirs(bstack111ll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠧࡿࠩ౜")), bstack111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨౝ"), bstack111_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ౞"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111_opy_ (u"ࠪࡻࠬ౟")):
        pass
      with open(file_path, bstack111_opy_ (u"ࠦࡼ࠱ࠢౠ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111_opy_ (u"ࠬࡸࠧౡ")) as bstack11111l11_opy_:
      bstack11ll1l1l_opy_ = json.load(bstack11111l11_opy_)
    if bstack1111ll11_opy_ in bstack11ll1l1l_opy_:
      bstack1l111111_opy_ = bstack11ll1l1l_opy_[bstack1111ll11_opy_][bstack111_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪౢ")]
      bstack11lll11l_opy_ = int(bstack1l111111_opy_) + 1
      bstack11111l1l_opy_(bstack1111ll11_opy_, bstack11lll11l_opy_, file_path)
      return bstack11lll11l_opy_
    else:
      bstack11111l1l_opy_(bstack1111ll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll111l_opy_.format(str(e)))
    return -1
def bstack1lllllll_opy_(config):
  if bstack111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩౣ") in config and config[bstack111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ౤")] not in bstack1llll1_opy_:
    return config[bstack111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౥")]
  elif bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ౦") in os.environ:
    return os.environ[bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ౧")]
  else:
    return None
def bstack1lll11111_opy_(config):
  if not bstack1lllllll_opy_(config) or not bstack1l1llllll_opy_(config):
    return True
  else:
    return False
def bstack1l111l1_opy_(config):
  if bstack1ll1l1ll_opy_() < version.parse(bstack111_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫ౨")):
    return False
  if bstack1ll1l1ll_opy_() >= version.parse(bstack111_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬ౩")):
    return True
  if bstack111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ౪") in config and config[bstack111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ౫")] == False:
    return False
  else:
    return True
def bstack11lll1ll_opy_(config, index = 0):
  global bstack1ll11l1_opy_
  bstack1l1lllll_opy_ = {}
  caps = bstack11ll_opy_ + bstack11ll1_opy_
  if bstack1ll11l1_opy_:
    caps += bstack1ll1l_opy_
  for key in config:
    if key in caps + [bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౬")]:
      continue
    bstack1l1lllll_opy_[key] = config[key]
  if bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭") in config:
    for bstack1lll11ll_opy_ in config[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౮")][index]:
      if bstack1lll11ll_opy_ in caps + [bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౯"), bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౰")]:
        continue
      bstack1l1lllll_opy_[bstack1lll11ll_opy_] = config[bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౱")][index][bstack1lll11ll_opy_]
  bstack1l1lllll_opy_[bstack111_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪ౲")] = socket.gethostname()
  return bstack1l1lllll_opy_
def bstack1111l111_opy_(config):
  global bstack1ll11l1_opy_
  bstack1l1l1ll_opy_ = {}
  caps = bstack11ll1_opy_
  if bstack1ll11l1_opy_:
    caps+= bstack1ll1l_opy_
  for key in caps:
    if key in config:
      bstack1l1l1ll_opy_[key] = config[key]
  return bstack1l1l1ll_opy_
def bstack11ll111l_opy_(bstack1l1lllll_opy_, bstack1l1l1ll_opy_):
  bstack1111l1l_opy_ = {}
  for key in bstack1l1lllll_opy_.keys():
    if key in bstack1l1ll_opy_:
      bstack1111l1l_opy_[bstack1l1ll_opy_[key]] = bstack1l1lllll_opy_[key]
    else:
      bstack1111l1l_opy_[key] = bstack1l1lllll_opy_[key]
  for key in bstack1l1l1ll_opy_:
    if key in bstack1l1ll_opy_:
      bstack1111l1l_opy_[bstack1l1ll_opy_[key]] = bstack1l1l1ll_opy_[key]
    else:
      bstack1111l1l_opy_[key] = bstack1l1l1ll_opy_[key]
  return bstack1111l1l_opy_
def bstack11ll1l_opy_(config, index = 0):
  global bstack1ll11l1_opy_
  caps = {}
  bstack1l1l1ll_opy_ = bstack1111l111_opy_(config)
  bstack1ll111l1_opy_ = bstack11ll1_opy_
  bstack1ll111l1_opy_ += bstack111l_opy_
  if bstack1ll11l1_opy_:
    bstack1ll111l1_opy_ += bstack1ll1l_opy_
  if bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౳") in config:
    if bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ౴") in config[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౵")][index]:
      caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౶")] = config[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౷")][index][bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ౸")]
    if bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౹") in config[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౺")][index]:
      caps[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ౻")] = str(config[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౼")][index][bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౽")])
    bstack1111ll1l_opy_ = {}
    for bstack1llll1l_opy_ in bstack1ll111l1_opy_:
      if bstack1llll1l_opy_ in config[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౾")][index]:
        if bstack1llll1l_opy_ == bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ౿"):
          bstack1111ll1l_opy_[bstack1llll1l_opy_] = str(config[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಀ")][index][bstack1llll1l_opy_] * 1.0)
        else:
          bstack1111ll1l_opy_[bstack1llll1l_opy_] = config[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಁ")][index][bstack1llll1l_opy_]
        del(config[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಂ")][index][bstack1llll1l_opy_])
    bstack1l1l1ll_opy_ = update(bstack1l1l1ll_opy_, bstack1111ll1l_opy_)
  bstack1l1lllll_opy_ = bstack11lll1ll_opy_(config, index)
  for bstack11l11lll_opy_ in bstack11ll1_opy_ + [bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩಃ"), bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭಄")]:
    if bstack11l11lll_opy_ in bstack1l1lllll_opy_:
      bstack1l1l1ll_opy_[bstack11l11lll_opy_] = bstack1l1lllll_opy_[bstack11l11lll_opy_]
      del(bstack1l1lllll_opy_[bstack11l11lll_opy_])
  if bstack1l111l1_opy_(config):
    bstack1l1lllll_opy_[bstack111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ಅ")] = True
    caps.update(bstack1l1l1ll_opy_)
    caps[bstack111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨಆ")] = bstack1l1lllll_opy_
  else:
    bstack1l1lllll_opy_[bstack111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨಇ")] = False
    caps.update(bstack11ll111l_opy_(bstack1l1lllll_opy_, bstack1l1l1ll_opy_))
    if bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಈ") in caps:
      caps[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಉ")] = caps[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩಊ")]
      del(caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಋ")])
    if bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧಌ") in caps:
      caps[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ಍")] = caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩಎ")]
      del(caps[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಏ")])
  return caps
def bstack11111lll_opy_():
  if bstack1ll1l1ll_opy_() <= version.parse(bstack111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪಐ")):
    return bstack1111l_opy_
  return bstack1l11ll_opy_
def bstack1lll1ll1_opy_(options):
  return hasattr(options, bstack111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ಑"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l111_opy_(options, bstack11ll11l_opy_):
  for bstack11llll1_opy_ in bstack11ll11l_opy_:
    if bstack11llll1_opy_ in [bstack111_opy_ (u"ࠬࡧࡲࡨࡵࠪಒ"), bstack111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪಓ")]:
      next
    if bstack11llll1_opy_ in options._experimental_options:
      options._experimental_options[bstack11llll1_opy_]= update(options._experimental_options[bstack11llll1_opy_], bstack11ll11l_opy_[bstack11llll1_opy_])
    else:
      options.add_experimental_option(bstack11llll1_opy_, bstack11ll11l_opy_[bstack11llll1_opy_])
  if bstack111_opy_ (u"ࠧࡢࡴࡪࡷࠬಔ") in bstack11ll11l_opy_:
    for arg in bstack11ll11l_opy_[bstack111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಕ")]:
      options.add_argument(arg)
    del(bstack11ll11l_opy_[bstack111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧಖ")])
  if bstack111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧಗ") in bstack11ll11l_opy_:
    for ext in bstack11ll11l_opy_[bstack111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨಘ")]:
      options.add_extension(ext)
    del(bstack11ll11l_opy_[bstack111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩಙ")])
def bstack11l1ll_opy_(options, bstack11ll1111_opy_):
  if bstack111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬಚ") in bstack11ll1111_opy_:
    for bstack111l1l1_opy_ in bstack11ll1111_opy_[bstack111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ಛ")]:
      if bstack111l1l1_opy_ in options._preferences:
        options._preferences[bstack111l1l1_opy_] = update(options._preferences[bstack111l1l1_opy_], bstack11ll1111_opy_[bstack111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧಜ")][bstack111l1l1_opy_])
      else:
        options.set_preference(bstack111l1l1_opy_, bstack11ll1111_opy_[bstack111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨಝ")][bstack111l1l1_opy_])
  if bstack111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨಞ") in bstack11ll1111_opy_:
    for arg in bstack11ll1111_opy_[bstack111_opy_ (u"ࠫࡦࡸࡧࡴࠩಟ")]:
      options.add_argument(arg)
def bstack1l11l1l1_opy_(options, bstack1lll1ll11_opy_):
  if bstack111_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ಠ") in bstack1lll1ll11_opy_:
    options.use_webview(bool(bstack1lll1ll11_opy_[bstack111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧಡ")]))
  bstack11l111_opy_(options, bstack1lll1ll11_opy_)
def bstack1l1111l_opy_(options, bstack1111lll_opy_):
  for bstack1111l1ll_opy_ in bstack1111lll_opy_:
    if bstack1111l1ll_opy_ in [bstack111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫಢ"), bstack111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಣ")]:
      next
    options.set_capability(bstack1111l1ll_opy_, bstack1111lll_opy_[bstack1111l1ll_opy_])
  if bstack111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧತ") in bstack1111lll_opy_:
    for arg in bstack1111lll_opy_[bstack111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨಥ")]:
      options.add_argument(arg)
  if bstack111_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨದ") in bstack1111lll_opy_:
    options.use_technology_preview(bool(bstack1111lll_opy_[bstack111_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩಧ")]))
def bstack1llllll11_opy_(options, bstack1l11ll1_opy_):
  for bstack1lll1ll_opy_ in bstack1l11ll1_opy_:
    if bstack1lll1ll_opy_ in [bstack111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪನ"), bstack111_opy_ (u"ࠧࡢࡴࡪࡷࠬ಩")]:
      next
    options._options[bstack1lll1ll_opy_] = bstack1l11ll1_opy_[bstack1lll1ll_opy_]
  if bstack111_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಪ") in bstack1l11ll1_opy_:
    for bstack111ll1l1_opy_ in bstack1l11ll1_opy_[bstack111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಫ")]:
      options.add_additional_option(
          bstack111ll1l1_opy_, bstack1l11ll1_opy_[bstack111_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧಬ")][bstack111ll1l1_opy_])
  if bstack111_opy_ (u"ࠫࡦࡸࡧࡴࠩಭ") in bstack1l11ll1_opy_:
    for arg in bstack1l11ll1_opy_[bstack111_opy_ (u"ࠬࡧࡲࡨࡵࠪಮ")]:
      options.add_argument(arg)
def bstack1ll111l1l_opy_(options, caps):
  if not hasattr(options, bstack111_opy_ (u"࠭ࡋࡆ࡛ࠪಯ")):
    return
  if options.KEY == bstack111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬರ") and options.KEY in caps:
    bstack11l111_opy_(options, caps[bstack111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ಱ")])
  elif options.KEY == bstack111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧಲ") and options.KEY in caps:
    bstack11l1ll_opy_(options, caps[bstack111_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨಳ")])
  elif options.KEY == bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ಴") and options.KEY in caps:
    bstack1l1111l_opy_(options, caps[bstack111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ವ")])
  elif options.KEY == bstack111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಶ") and options.KEY in caps:
    bstack1l11l1l1_opy_(options, caps[bstack111_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨಷ")])
  elif options.KEY == bstack111_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಸ") and options.KEY in caps:
    bstack1llllll11_opy_(options, caps[bstack111_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨಹ")])
def bstack1lll111l1_opy_(caps):
  global bstack1ll11l1_opy_
  if bstack1ll11l1_opy_:
    if bstack1llll1l1l_opy_() < version.parse(bstack111_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩ಺")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ಻")
    if bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧ಼ࠪ") in caps:
      browser = caps[bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಽ")]
    elif bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨಾ") in caps:
      browser = caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩಿ")]
    browser = str(browser).lower()
    if browser == bstack111_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩೀ") or browser == bstack111_opy_ (u"ࠪ࡭ࡵࡧࡤࠨು"):
      browser = bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫೂ")
    if browser == bstack111_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭ೃ"):
      browser = bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ೄ")
    if browser not in [bstack111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ೅"), bstack111_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ೆ"), bstack111_opy_ (u"ࠩ࡬ࡩࠬೇ"), bstack111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪೈ"), bstack111_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ೉")]:
      return None
    try:
      package = bstack111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧೊ").format(browser)
      name = bstack111_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧೋ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll1ll1_opy_(options):
        return None
      for bstack11l11lll_opy_ in caps.keys():
        options.set_capability(bstack11l11lll_opy_, caps[bstack11l11lll_opy_])
      bstack1ll111l1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1ll1lll_opy_(options, bstack1l111ll_opy_):
  if not bstack1lll1ll1_opy_(options):
    return
  for bstack11l11lll_opy_ in bstack1l111ll_opy_.keys():
    if bstack11l11lll_opy_ in bstack111l_opy_:
      next
    if bstack11l11lll_opy_ in options._caps and type(options._caps[bstack11l11lll_opy_]) in [dict, list]:
      options._caps[bstack11l11lll_opy_] = update(options._caps[bstack11l11lll_opy_], bstack1l111ll_opy_[bstack11l11lll_opy_])
    else:
      options.set_capability(bstack11l11lll_opy_, bstack1l111ll_opy_[bstack11l11lll_opy_])
  bstack1ll111l1l_opy_(options, bstack1l111ll_opy_)
  if bstack111_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ೌ") in options._caps:
    if options._caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ್࠭")] and options._caps[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ೎")].lower() != bstack111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ೏"):
      del options._caps[bstack111_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ೐")]
def bstack1llll1l1_opy_(proxy_config):
  if bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ೑") in proxy_config:
    proxy_config[bstack111_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨ೒")] = proxy_config[bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ೓")]
    del(proxy_config[bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ೔")])
  if bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬೕ") in proxy_config and proxy_config[bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ೖ")].lower() != bstack111_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ೗"):
    proxy_config[bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ೘")] = bstack111_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭೙")
  if bstack111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ೚") in proxy_config:
    proxy_config[bstack111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ೛")] = bstack111_opy_ (u"ࠩࡳࡥࡨ࠭೜")
  return proxy_config
def bstack1ll11llll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩೝ") in config:
    return proxy
  config[bstack111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪೞ")] = bstack1llll1l1_opy_(config[bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ೟")])
  if proxy == None:
    proxy = Proxy(config[bstack111_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬೠ")])
  return proxy
def bstack111ll111_opy_(self):
  global CONFIG
  global bstack1l1111l1_opy_
  if bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪೡ") in CONFIG:
    return CONFIG[bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫೢ")]
  elif bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ೣ") in CONFIG:
    return CONFIG[bstack111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ೤")]
  else:
    return bstack1l1111l1_opy_(self)
def bstack1lll1llll_opy_():
  global CONFIG
  return bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ೥") in CONFIG or bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ೦") in CONFIG
def bstack1l11111_opy_(config):
  if not bstack1lll1llll_opy_():
    return
  if config.get(bstack111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ೧")):
    return config.get(bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ೨"))
  if config.get(bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ೩")):
    return config.get(bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭೪"))
def bstack1111l1_opy_():
  return bstack1lll1llll_opy_() and bstack1ll1l1ll_opy_() >= version.parse(bstack111l1_opy_)
def bstack1l1l111_opy_(config):
  if bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ೫") in config:
    if str(config[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ೬")]).lower() == bstack111_opy_ (u"ࠬࡺࡲࡶࡧࠪ೭"):
      return True
    else:
      return False
  elif bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ೮") in os.environ:
    if str(os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ೯")]).lower() == bstack111_opy_ (u"ࠨࡶࡵࡹࡪ࠭೰"):
      return True
    else:
      return False
  else:
    return False
def bstack1ll1lll1_opy_(config):
  if bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ೱ") in config:
    return config[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧೲ")]
  if bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪೳ") in config:
    return config[bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ೴")]
  return {}
def bstack11l11ll1_opy_(caps):
  global bstack1l1l11ll_opy_
  if bstack111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ೵") in caps:
    caps[bstack111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ೶")][bstack111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ೷")] = True
    if bstack1l1l11ll_opy_:
      caps[bstack111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ೸")][bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೹")] = bstack1l1l11ll_opy_
  else:
    caps[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ೺")] = True
    if bstack1l1l11ll_opy_:
      caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೻")] = bstack1l1l11ll_opy_
def bstack1l1ll1l1_opy_():
  global CONFIG
  if bstack1l1l111_opy_(CONFIG):
    bstack11lll1l_opy_ = bstack1ll1lll1_opy_(CONFIG)
    bstack1l11lll1_opy_(bstack1l1llllll_opy_(CONFIG), bstack11lll1l_opy_)
def bstack1l11lll1_opy_(key, bstack11lll1l_opy_):
  global bstack11111ll1_opy_
  logger.info(bstack1ll1llll_opy_)
  try:
    bstack11111ll1_opy_ = Local()
    bstack111l1l_opy_ = {bstack111_opy_ (u"࠭࡫ࡦࡻࠪ೼"): key}
    bstack111l1l_opy_.update(bstack11lll1l_opy_)
    logger.debug(bstack1l1ll1ll1_opy_.format(str(bstack111l1l_opy_)))
    bstack11111ll1_opy_.start(**bstack111l1l_opy_)
    if bstack11111ll1_opy_.isRunning():
      logger.info(bstack1111lll1_opy_)
  except Exception as e:
    bstack1ll1llll1_opy_(bstack1llll1ll1_opy_.format(str(e)))
def bstack1ll1lll_opy_():
  global bstack11111ll1_opy_
  if bstack11111ll1_opy_.isRunning():
    logger.info(bstack111l1ll1_opy_)
    bstack11111ll1_opy_.stop()
  bstack11111ll1_opy_ = None
def bstack1l1lll11_opy_():
  global bstack11l1lll1_opy_
  if bstack11l1lll1_opy_:
    logger.warning(bstack1lll11l1_opy_.format(str(bstack11l1lll1_opy_)))
  logger.info(bstack1lll1l11_opy_)
  global bstack11111ll1_opy_
  if bstack11111ll1_opy_:
    bstack1ll1lll_opy_()
  logger.info(bstack1ll1ll1l1_opy_)
  bstack1l1l1ll1_opy_()
def bstack11l11l1l_opy_(self, *args):
  logger.error(bstack111lllll_opy_)
  bstack1l1lll11_opy_()
  sys.exit(1)
def bstack1ll1llll1_opy_(err):
  logger.critical(bstack1ll1l1l11_opy_.format(str(err)))
  bstack1l1l1ll1_opy_(bstack1ll1l1l11_opy_.format(str(err)))
  atexit.unregister(bstack1l1lll11_opy_)
  sys.exit(1)
def bstack1l1111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l1ll1_opy_(message)
  atexit.unregister(bstack1l1lll11_opy_)
  sys.exit(1)
def bstack1111l11l_opy_():
  global CONFIG
  CONFIG = bstack1l1l11l_opy_()
  CONFIG = bstack11111ll_opy_(CONFIG)
  CONFIG = bstack111l1l1l_opy_(CONFIG)
  if bstack1lll11111_opy_(CONFIG):
    bstack1ll1llll1_opy_(bstack1l111l11_opy_)
  CONFIG[bstack111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೽")] = bstack1lllllll_opy_(CONFIG)
  CONFIG[bstack111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ೾")] = bstack1l1llllll_opy_(CONFIG)
  if bstack1l1lll1l1_opy_(CONFIG):
    CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ೿")] = bstack1l1lll1l1_opy_(CONFIG)
    if not os.getenv(bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭ഀ")):
      if os.getenv(bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨഁ")):
        CONFIG[bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧം")] = os.getenv(bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪഃ"))
      else:
        bstack11l1ll11_opy_()
    else:
      if bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩഄ") in CONFIG:
        del(CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഅ")])
  bstack11l1l1ll_opy_()
  bstack1ll1111ll_opy_()
  if bstack1ll11l1_opy_:
    CONFIG[bstack111_opy_ (u"ࠩࡤࡴࡵ࠭ആ")] = bstack11llll_opy_(CONFIG)
    logger.info(bstack1llll1ll_opy_.format(CONFIG[bstack111_opy_ (u"ࠪࡥࡵࡶࠧഇ")]))
def bstack1ll1111ll_opy_():
  global CONFIG
  global bstack1ll11l1_opy_
  if bstack111_opy_ (u"ࠫࡦࡶࡰࠨഈ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1111_opy_(e, bstack1l1lll1l_opy_)
    bstack1ll11l1_opy_ = True
def bstack11llll_opy_(config):
  bstack1lll1111_opy_ = bstack111_opy_ (u"ࠬ࠭ഉ")
  app = config[bstack111_opy_ (u"࠭ࡡࡱࡲࠪഊ")]
  if isinstance(config[bstack111_opy_ (u"ࠧࡢࡲࡳࠫഋ")], str):
    if os.path.splitext(app)[1] in bstack1l1l1_opy_:
      if os.path.exists(app):
        bstack1lll1111_opy_ = bstack11ll11_opy_(config, app)
      elif bstack1111l11_opy_(app):
        bstack1lll1111_opy_ = app
      else:
        bstack1ll1llll1_opy_(bstack111111l_opy_.format(app))
    else:
      if bstack1111l11_opy_(app):
        bstack1lll1111_opy_ = app
      elif os.path.exists(app):
        bstack1lll1111_opy_ = bstack11ll11_opy_(app)
      else:
        bstack1ll1llll1_opy_(bstack11ll111_opy_)
  else:
    if len(app) > 2:
      bstack1ll1llll1_opy_(bstack1ll11lll1_opy_)
    elif len(app) == 2:
      if bstack111_opy_ (u"ࠨࡲࡤࡸ࡭࠭ഌ") in app and bstack111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ഍") in app:
        if os.path.exists(app[bstack111_opy_ (u"ࠪࡴࡦࡺࡨࠨഎ")]):
          bstack1lll1111_opy_ = bstack11ll11_opy_(config, app[bstack111_opy_ (u"ࠫࡵࡧࡴࡩࠩഏ")], app[bstack111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨഐ")])
        else:
          bstack1ll1llll1_opy_(bstack111111l_opy_.format(app))
      else:
        bstack1ll1llll1_opy_(bstack1ll11lll1_opy_)
    else:
      for key in app:
        if key in bstack1l111_opy_:
          if key == bstack111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ഑"):
            if os.path.exists(app[key]):
              bstack1lll1111_opy_ = bstack11ll11_opy_(config, app[key])
            else:
              bstack1ll1llll1_opy_(bstack111111l_opy_.format(app))
          else:
            bstack1lll1111_opy_ = app[key]
        else:
          bstack1ll1llll1_opy_(bstack1l1l111l_opy_)
  return bstack1lll1111_opy_
def bstack1111l11_opy_(bstack1lll1111_opy_):
  import re
  bstack11111111_opy_ = re.compile(bstack111_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢഒ"))
  bstack1ll111l11_opy_ = re.compile(bstack111_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧഓ"))
  if bstack111_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨഔ") in bstack1lll1111_opy_ or re.fullmatch(bstack11111111_opy_, bstack1lll1111_opy_) or re.fullmatch(bstack1ll111l11_opy_, bstack1lll1111_opy_):
    return True
  else:
    return False
def bstack11ll11_opy_(config, path, bstack111l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111_opy_ (u"ࠪࡶࡧ࠭ക")).read()).hexdigest()
  bstack11l111l_opy_ = bstack1l11l11_opy_(md5_hash)
  bstack1lll1111_opy_ = None
  if bstack11l111l_opy_:
    logger.info(bstack1ll1ll111_opy_.format(bstack11l111l_opy_, md5_hash))
    return bstack11l111l_opy_
  bstack1ll1l1111_opy_ = MultipartEncoder(
    fields={
        bstack111_opy_ (u"ࠫ࡫࡯࡬ࡦࠩഖ"): (os.path.basename(path), open(os.path.abspath(path), bstack111_opy_ (u"ࠬࡸࡢࠨഗ")), bstack111_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪഘ")),
        bstack111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪങ"): bstack111l11_opy_
    }
  )
  response = requests.post(bstack1lll1_opy_, data=bstack1ll1l1111_opy_,
                         headers={bstack111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧച"): bstack1ll1l1111_opy_.content_type}, auth=(bstack1lllllll_opy_(config), bstack1l1llllll_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack1lll1111_opy_ = res[bstack111_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪഛ")]
    logger.info(bstack11111l1_opy_.format(bstack1lll1111_opy_))
    bstack1l1llll_opy_(md5_hash, bstack1lll1111_opy_)
  except ValueError as err:
    bstack1ll1llll1_opy_(bstack11l1ll1_opy_.format(str(err)))
  return bstack1lll1111_opy_
def bstack11l1l1ll_opy_():
  global CONFIG
  global bstack111ll1l_opy_
  bstack1l1ll11_opy_ = 1
  if bstack111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪജ") in CONFIG:
    bstack1l1ll11_opy_ = CONFIG[bstack111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫഝ")]
  bstack1l1ll1l_opy_ = 0
  if bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഞ") in CONFIG:
    bstack1l1ll1l_opy_ = len(CONFIG[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩട")])
  bstack111ll1l_opy_ = int(bstack1l1ll11_opy_) * int(bstack1l1ll1l_opy_)
def bstack1l11l11_opy_(md5_hash):
  bstack1ll11111l_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠧࡿࠩഠ")), bstack111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨഡ"), bstack111_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪഢ"))
  if os.path.exists(bstack1ll11111l_opy_):
    bstack1ll11l1ll_opy_ = json.load(open(bstack1ll11111l_opy_,bstack111_opy_ (u"ࠪࡶࡧ࠭ണ")))
    if md5_hash in bstack1ll11l1ll_opy_:
      bstack11l1l1l1_opy_ = bstack1ll11l1ll_opy_[md5_hash]
      bstack1lll1lll1_opy_ = datetime.datetime.now()
      bstack111lll1_opy_ = datetime.datetime.strptime(bstack11l1l1l1_opy_[bstack111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧത")], bstack111_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩഥ"))
      if (bstack1lll1lll1_opy_ - bstack111lll1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l1l1l1_opy_[bstack111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫദ")]):
        return None
      return bstack11l1l1l1_opy_[bstack111_opy_ (u"ࠧࡪࡦࠪധ")]
  else:
    return None
def bstack1l1llll_opy_(md5_hash, bstack1lll1111_opy_):
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠨࢀࠪന")), bstack111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩഩ"))
  if not os.path.exists(bstack111ll11_opy_):
    os.makedirs(bstack111ll11_opy_)
  bstack1ll11111l_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠪࢂࠬപ")), bstack111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫഫ"), bstack111_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ബ"))
  bstack111111ll_opy_ = {
    bstack111_opy_ (u"࠭ࡩࡥࠩഭ"): bstack1lll1111_opy_,
    bstack111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪമ"): datetime.datetime.strftime(datetime.datetime.now(), bstack111_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬയ")),
    bstack111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧര"): str(__version__)
  }
  if os.path.exists(bstack1ll11111l_opy_):
    bstack1ll11l1ll_opy_ = json.load(open(bstack1ll11111l_opy_,bstack111_opy_ (u"ࠪࡶࡧ࠭റ")))
  else:
    bstack1ll11l1ll_opy_ = {}
  bstack1ll11l1ll_opy_[md5_hash] = bstack111111ll_opy_
  with open(bstack1ll11111l_opy_, bstack111_opy_ (u"ࠦࡼ࠱ࠢല")) as outfile:
    json.dump(bstack1ll11l1ll_opy_, outfile)
def bstack1ll1ll1ll_opy_(self):
  return
def bstack111l1111_opy_(self):
  return
def bstack1ll11111_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack11ll11l1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll1ll1_opy_
  global bstack111ll11l_opy_
  global bstack11l1111l_opy_
  global bstack1lll1l1l1_opy_
  global bstack1ll1111l1_opy_
  global bstack1lllll11l_opy_
  CONFIG[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧള")] = str(bstack1ll1111l1_opy_) + str(__version__)
  command_executor = bstack11111lll_opy_()
  logger.debug(bstack1llll11l_opy_.format(command_executor))
  proxy = bstack1ll11llll_opy_(CONFIG, proxy)
  bstack1lllll1l_opy_ = 0 if bstack111ll11l_opy_ < 0 else bstack111ll11l_opy_
  if bstack1lll1l1l1_opy_ is True:
    bstack1lllll1l_opy_ = int(threading.current_thread().getName())
  bstack1l111ll_opy_ = bstack11ll1l_opy_(CONFIG, bstack1lllll1l_opy_)
  logger.debug(bstack11l1l111_opy_.format(str(bstack1l111ll_opy_)))
  if bstack1l1l111_opy_(CONFIG):
    bstack11l11ll1_opy_(bstack1l111ll_opy_)
  if desired_capabilities:
    bstack111llll1_opy_ = bstack11ll1l_opy_(bstack11111ll_opy_(desired_capabilities))
    if bstack111llll1_opy_:
      bstack1l111ll_opy_ = update(bstack111llll1_opy_, bstack1l111ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1ll1lll_opy_(options, bstack1l111ll_opy_)
  if not options:
    options = bstack1lll111l1_opy_(bstack1l111ll_opy_)
  if options and bstack1ll1l1ll_opy_() >= version.parse(bstack111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬഴ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll1l1ll_opy_() < version.parse(bstack111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭വ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l111ll_opy_)
  logger.info(bstack11l1l11l_opy_)
  if bstack1ll1l1ll_opy_() >= version.parse(bstack111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧശ")):
    bstack1lllll11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1l1ll_opy_() >= version.parse(bstack111_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩഷ")):
    bstack1lllll11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lllll11l_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack1ll1ll1_opy_ = self.session_id
  if bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭സ") in CONFIG and bstack111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩഹ") in CONFIG[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഺ")][bstack1lllll1l_opy_]:
    bstack11l1111l_opy_ = CONFIG[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ഻ࠩ")][bstack1lllll1l_opy_][bstack111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩ഼ࠬ")]
  logger.debug(bstack1ll1l1lll_opy_.format(bstack1ll1ll1_opy_))
def bstack1l1lllll1_opy_(self, url):
  global bstack1l11ll1l_opy_
  try:
    bstack1lll1ll1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11lll_opy_.format(str(err)))
  bstack1l11ll1l_opy_(self, url)
def bstack1ll1ll11_opy_(self, test):
  global CONFIG
  global bstack1ll1ll1_opy_
  global bstack1ll1lll1l_opy_
  global bstack11l1111l_opy_
  global bstack1ll111ll_opy_
  if bstack1ll1ll1_opy_:
    try:
      data = {}
      bstack1l1lll11l_opy_ = None
      if test:
        bstack1l1lll11l_opy_ = str(test.data)
      if bstack1l1lll11l_opy_ and not bstack11l1111l_opy_:
        data[bstack111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഽ")] = bstack1l1lll11l_opy_
      if bstack1ll1lll1l_opy_:
        if bstack1ll1lll1l_opy_.status == bstack111_opy_ (u"ࠩࡓࡅࡘ࡙ࠧാ"):
          data[bstack111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪി")] = bstack111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫീ")
        elif bstack1ll1lll1l_opy_.status == bstack111_opy_ (u"ࠬࡌࡁࡊࡎࠪു"):
          data[bstack111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ൂ")] = bstack111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧൃ")
          if bstack1ll1lll1l_opy_.message:
            data[bstack111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨൄ")] = str(bstack1ll1lll1l_opy_.message)
      user = CONFIG[bstack111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൅")]
      key = CONFIG[bstack111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭െ")]
      url = bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩേ").format(user, key, bstack1ll1ll1_opy_)
      headers = {
        bstack111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫൈ"): bstack111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ൉"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111lll1l_opy_.format(str(e)))
  bstack1ll111ll_opy_(self, test)
def bstack11l11ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111l1l11_opy_
  bstack111l1l11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1lll1l_opy_
  bstack1ll1lll1l_opy_ = self._test
def bstack1l1lll1ll_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack111_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢൊ"), bstack111_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧോ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack111_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶࠧൌ"), bstack111_opy_ (u"ࠥ࠲്ࠧ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack111_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥൎ"))))
  if not files:
    pabot._write(bstack111_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧ൏") % outs_dir, pabot.Color.YELLOW)
    return bstack111_opy_ (u"ࠨࠢ൐")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1llll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ൑") in options:
    del options[bstack111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ൒")]
  if ROBOT_VERSION < bstack111_opy_ (u"ࠤ࠷࠲࠵ࠨ൓"):
    stats = {
      bstack111_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧൔ"): {bstack111_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥൕ"): 0, bstack111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧൖ"): 0, bstack111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨൗ"): 0},
      bstack111_opy_ (u"ࠢࡢ࡮࡯ࠦ൘"): {bstack111_opy_ (u"ࠣࡶࡲࡸࡦࡲࠢ൙"): 0, bstack111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ൚"): 0, bstack111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ൛"): 0},
    }
  else:
    stats = {
      bstack111_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥ൜"): 0,
      bstack111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ൝"): 0,
      bstack111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ൞"): 0,
      bstack111_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣൟ"): 0,
    }
  if pabot_args[bstack111_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢൠ")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack111_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣൡ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack111_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨൢ")], pabot_args[bstack111_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧൣ")]
      )
      outputs += [
        bstack1l1lll1ll_opy_(
          os.path.join(outs_dir, str(index)+ bstack111_opy_ (u"ࠧ࠵ࠢ൤")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack111_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨ൥"), bstack111_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨ൦") % index),
        )
      ]
    if bstack111_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣ൧") not in options:
      options[bstack111_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤ൨")] = bstack111_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢ൩")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lllll1ll_opy_(self, ff_profile_dir):
  global bstack1l1ll1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll1ll_opy_(self, ff_profile_dir)
def bstack1ll111lll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l11ll_opy_
  bstack1l1llll1l_opy_ = []
  if bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ൪") in CONFIG:
    bstack1l1llll1l_opy_ = CONFIG[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൫")]
  bstack111l111_opy_ = len(suite_group) * len(pabot_args[bstack111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ൬")] or [(bstack111_opy_ (u"ࠢࠣ൭"), None)]) * len(bstack1l1llll1l_opy_)
  pabot_args[bstack111_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢ൮")] = []
  for q in range(bstack111l111_opy_):
    pabot_args[bstack111_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ൯")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ൰")],
      pabot_args[bstack111_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ൱")],
      argfile,
      pabot_args.get(bstack111_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ൲")),
      pabot_args[bstack111_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ൳")],
      platform[0],
      bstack1l1l11ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ൴")] or [(bstack111_opy_ (u"ࠣࠤ൵"), None)]
    for platform in enumerate(bstack1l1llll1l_opy_)
  ]
def bstack1ll111111_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1llll11_opy_=bstack111_opy_ (u"ࠩࠪ൶")):
  global bstack11ll1ll1_opy_
  self.platform_index = platform_index
  self.bstack1ll1l1l1_opy_ = bstack1llll11_opy_
  bstack11ll1ll1_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll11l11l_opy_
  global bstack1llll111l_opy_
  if not bstack111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ൷") in item.options:
    item.options[bstack111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭൸")] = []
  for v in item.options[bstack111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ൹")]:
    if bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬൺ") in v:
      item.options[bstack111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩൻ")].remove(v)
  item.options[bstack111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪർ")].insert(0, bstack111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫൽ").format(item.platform_index))
  item.options[bstack111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬൾ")].insert(0, bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫൿ").format(item.bstack1ll1l1l1_opy_))
  if bstack1llll111l_opy_:
    item.options[bstack111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ඀")].insert(0, bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡏࡏࡈࡌࡋࡋࡏࡌࡆ࠼ࡾࢁࠬඁ").format(bstack1llll111l_opy_))
  return bstack1ll11l11l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lllll11_opy_
  global bstack1llll111l_opy_
  if bstack1llll111l_opy_:
    command[0] = command[0].replace(bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ං"), bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠢࠪඃ") + bstack1llll111l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ඄"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඅ"), 1)
  return bstack1lllll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1l11l1_opy_
  bstack1lll1l11l_opy_ = bstack1ll1l11l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack111_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫආ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩඇ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1l11l_opy_
def bstack1ll11lll_opy_(self, name, context, *args):
  global bstack1ll11l111_opy_
  if name in [bstack111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧඈ"), bstack111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩඉ")]:
    bstack1ll11l111_opy_(self, name, context, *args)
  if name == bstack111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩඊ"):
    try:
      bstack1lllllll1_opy_ = str(self.feature.name)
      context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧඋ") + json.dumps(bstack1lllllll1_opy_) + bstack111_opy_ (u"ࠪࢁࢂ࠭ඌ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫඍ").format(str(e)))
  if name == bstack111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧඎ"):
    try:
      if not hasattr(self, bstack111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඏ")):
        self.driver_before_scenario = True
      bstack111l1lll_opy_ = args[0].name
      bstack11l11l1_opy_ = bstack1lllllll1_opy_ = str(self.feature.name)
      bstack1lllllll1_opy_ = bstack11l11l1_opy_ + bstack111_opy_ (u"ࠧࠡ࠯ࠣࠫඐ") + bstack111l1lll_opy_
      if self.driver_before_scenario:
        context.browser.execute_script(bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭එ") + json.dumps(bstack1lllllll1_opy_) + bstack111_opy_ (u"ࠩࢀࢁࠬඒ"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫඓ").format(str(e)))
  if name == bstack111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬඔ"):
    try:
      bstack11ll1lll_opy_ = args[0].status.name
      if str(bstack11ll1lll_opy_).lower() == bstack111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬඕ"):
        bstack1ll1l1ll1_opy_ = bstack111_opy_ (u"࠭ࠧඖ")
        bstack111ll1_opy_ = bstack111_opy_ (u"ࠧࠨ඗")
        bstack11l1l1_opy_ = bstack111_opy_ (u"ࠨࠩ඘")
        try:
          import traceback
          bstack1ll1l1ll1_opy_ = self.exception.__class__.__name__
          bstack1lll1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111ll1_opy_ = bstack111_opy_ (u"ࠩࠣࠫ඙").join(bstack1lll1l1_opy_)
          bstack11l1l1_opy_ = bstack1lll1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l11l1_opy_.format(str(e)))
        bstack1ll1l1ll1_opy_ += bstack11l1l1_opy_
        context.browser.execute_script(bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨක") + json.dumps(str(args[0].name) + bstack111_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥඛ") + str(bstack111ll1_opy_)) + bstack111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬග"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ඝ") + json.dumps(bstack111_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦඞ") + str(bstack1ll1l1ll1_opy_)) + bstack111_opy_ (u"ࠨࡿࢀࠫඟ"))
      else:
        context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧච") + json.dumps(str(args[0].name) + bstack111_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢඡ")) + bstack111_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪජ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡰࡢࡵࡶࡩࡩࠨࡽࡾࠩඣ"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨඤ").format(str(e)))
  if name == bstack111_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧඥ"):
    try:
      if context.failed is True:
        bstack1l1ll1l1l_opy_ = []
        bstack11lll1l1_opy_ = []
        bstack1ll111ll1_opy_ = []
        bstack1l11111l_opy_ = bstack111_opy_ (u"ࠨࠩඦ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1ll1l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lll1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1l11l1l_opy_ = bstack111_opy_ (u"ࠩࠣࠫට").join(bstack1lll1l1_opy_)
            bstack11lll1l1_opy_.append(bstack1l11l1l_opy_)
            bstack1ll111ll1_opy_.append(bstack1lll1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l11l1_opy_.format(str(e)))
        bstack1ll1l1ll1_opy_ = bstack111_opy_ (u"ࠪࠫඨ")
        for i in range(len(bstack1l1ll1l1l_opy_)):
          bstack1ll1l1ll1_opy_ += bstack1l1ll1l1l_opy_[i] + bstack1ll111ll1_opy_[i] + bstack111_opy_ (u"ࠫࡡࡴࠧඩ")
        bstack1l11111l_opy_ = bstack111_opy_ (u"ࠬࠦࠧඪ").join(bstack11lll1l1_opy_)
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫණ") + json.dumps(bstack1l11111l_opy_) + bstack111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧඬ"))
          context.browser.execute_script(bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨත") + json.dumps(bstack111_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢථ") + str(bstack1ll1l1ll1_opy_)) + bstack111_opy_ (u"ࠪࢁࢂ࠭ද"))
      else:
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩධ") + json.dumps(bstack111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣන") + str(self.feature.name) + bstack111_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ඲")) + bstack111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ඳ"))
          context.browser.execute_script(bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬප"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫඵ").format(str(e)))
  if name in [bstack111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪබ"), bstack111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬභ")]:
    bstack1ll11l111_opy_(self, name, context, *args)
def bstack1l11l11l_opy_(bstack1lll1l111_opy_):
  global bstack1ll1111l1_opy_
  bstack1ll1111l1_opy_ = bstack1lll1l111_opy_
  logger.info(bstack11l111ll_opy_.format(bstack1ll1111l1_opy_.split(bstack111_opy_ (u"ࠬ࠳ࠧම"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1l1111_opy_(e, bstack1llll11ll_opy_)
  Service.start = bstack1ll1ll1ll_opy_
  Service.stop = bstack111l1111_opy_
  webdriver.Remote.__init__ = bstack11ll11l1_opy_
  webdriver.Remote.get = bstack1l1lllll1_opy_
  WebDriver.close = bstack1ll11111_opy_
  if bstack1111l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111ll111_opy_
    except Exception as e:
      logger.error(bstack1l1l1l11_opy_.format(str(e)))
  if (bstack111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඹ") in str(bstack1lll1l111_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1l1111_opy_(e, bstack1ll1ll1l_opy_)
    Output.end_test = bstack1ll1ll11_opy_
    TestStatus.__init__ = bstack11l11ll_opy_
    WebDriverCreator._get_ff_profile = bstack1lllll1ll_opy_
    QueueItem.__init__ = bstack1ll111111_opy_
    pabot._create_items = bstack1ll111lll_opy_
    pabot._run = bstack11ll1l11_opy_
    pabot._create_command_for_execution = bstack1ll1111_opy_
    pabot._report_results = bstack1llll11l1_opy_
  if bstack111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧය") in str(bstack1lll1l111_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1111_opy_(e, bstack11l111l1_opy_)
    Runner.run_hook = bstack1ll11lll_opy_
    Step.run = bstack1ll1l1l_opy_
def bstack1ll1l1l1l_opy_():
  global CONFIG
  if bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨර") in CONFIG and int(CONFIG[bstack111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ඼")]) > 1:
    logger.warn(bstack1ll1ll11l_opy_)
def bstack1ll11l1l1_opy_(bstack1l1l1lll_opy_, index):
  bstack1l11l11l_opy_(bstack11l1l_opy_)
  exec(open(bstack1l1l1lll_opy_).read())
def bstack1l11l111_opy_(arg):
  global CONFIG
  bstack1l11l11l_opy_(bstack1ll1l1_opy_)
  os.environ[bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫල")] = CONFIG[bstack111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭඾")]
  os.environ[bstack111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ඿")] = CONFIG[bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩව")]
  from _pytest.config import main as bstack11llllll_opy_
  bstack11llllll_opy_(arg)
def bstack11llll11_opy_(arg):
  bstack1l11l11l_opy_(bstack11l11_opy_)
  from behave.__main__ import main as bstack11lll1_opy_
  bstack11lll1_opy_(arg)
def bstack11lllll_opy_():
  logger.info(bstack111l111l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ශ"), help=bstack111_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩෂ"))
  parser.add_argument(bstack111_opy_ (u"ࠩ࠰ࡹࠬස"), bstack111_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧහ"), help=bstack111_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪළ"))
  parser.add_argument(bstack111_opy_ (u"ࠬ࠳࡫ࠨෆ"), bstack111_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬ෇"), help=bstack111_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨ෈"))
  parser.add_argument(bstack111_opy_ (u"ࠨ࠯ࡩࠫ෉"), bstack111_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ්ࠧ"), help=bstack111_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෋"))
  bstack11l11l_opy_ = parser.parse_args()
  try:
    bstack11lll11_opy_ = bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ෌")
    if bstack11l11l_opy_.framework and bstack11l11l_opy_.framework not in (bstack111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෍"), bstack111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ෎")):
      bstack11lll11_opy_ = bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ා")
    bstack111l11l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11lll11_opy_)
    bstack1111111_opy_ = open(bstack111l11l1_opy_, bstack111_opy_ (u"ࠨࡴࠪැ"))
    bstack1ll1l111l_opy_ = bstack1111111_opy_.read()
    bstack1111111_opy_.close()
    if bstack11l11l_opy_.username:
      bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩෑ"), bstack11l11l_opy_.username)
    if bstack11l11l_opy_.key:
      bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬි"), bstack11l11l_opy_.key)
    if bstack11l11l_opy_.framework:
      bstack1ll1l111l_opy_ = bstack1ll1l111l_opy_.replace(bstack111_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬී"), bstack11l11l_opy_.framework)
    file_name = bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨු")
    file_path = os.path.abspath(file_name)
    bstack1lll11l_opy_ = open(file_path, bstack111_opy_ (u"࠭ࡷࠨ෕"))
    bstack1lll11l_opy_.write(bstack1ll1l111l_opy_)
    bstack1lll11l_opy_.close()
    logger.info(bstack1llllll1_opy_)
    try:
      os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩූ")] = bstack11l11l_opy_.framework if bstack11l11l_opy_.framework != None else bstack111_opy_ (u"ࠣࠤ෗")
      config = yaml.safe_load(bstack1ll1l111l_opy_)
      config[bstack111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩෘ")] = bstack111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩෙ")
      bstack11l1l1l_opy_(bstack111ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1lllll1l1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1lll_opy_.format(str(e)))
def bstack11l1l1l_opy_(bstack1l1l1l1_opy_, config, bstack111lll11_opy_ = {}):
  global bstack1ll11l1l_opy_
  if not config:
    return
  bstack1lll111ll_opy_ = bstack1ll11_opy_ if not bstack1ll11l1l_opy_ else ( bstack1ll111_opy_ if bstack111_opy_ (u"ࠫࡦࡶࡰࠨේ") in config else bstack1l1lll_opy_ )
  data = {
    bstack111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧෛ"): bstack1lllllll_opy_(config),
    bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩො"): bstack1l1llllll_opy_(config),
    bstack111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫෝ"): bstack1l1l1l1_opy_,
    bstack111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫෞ"): {
      bstack111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧෟ"): str(config[bstack111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ෠")]) if bstack111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ෡") in config else bstack111_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ෢"),
      bstack111_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨ෣"): bstack1111ll_opy_(os.getenv(bstack111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ෤"), bstack111_opy_ (u"ࠣࠤ෥"))),
      bstack111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ෦"): bstack111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෧"),
      bstack111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ෨"): bstack1lll111ll_opy_,
      bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෩"): config[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ෪")] if bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ෫") in config else bstack111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ෬"),
      bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ෭"): str(config[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ෮")]) if bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭෯") in config else bstack111_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ෰"),
      bstack111_opy_ (u"࠭࡯ࡴࠩ෱"): sys.platform,
      bstack111_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩෲ"): socket.gethostname()
    }
  }
  update(data[bstack111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫෳ")], bstack111lll11_opy_)
  try:
    response = bstack1ll11ll11_opy_(bstack111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ෴"), bstack11lll_opy_, data, config)
    if response:
      logger.debug(bstack11l11l11_opy_.format(bstack1l1l1l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111111_opy_.format(str(e)))
def bstack1ll11ll11_opy_(type, url, data, config):
  bstack1ll1l11_opy_ = bstack1llll_opy_.format(url)
  proxy = bstack1l11111_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭෵")):
    proxies = {
      bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ෶"): proxy
    }
  if config.get(bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ෷")):
    proxies = {
      bstack111_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ෸"): proxy
    }
  if type == bstack111_opy_ (u"ࠧࡑࡑࡖࡘࠬ෹"):
    response = requests.post(bstack1ll1l11_opy_, json=data,
                    headers={bstack111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ෺"): bstack111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ෻")}, auth=(bstack1lllllll_opy_(config), bstack1l1llllll_opy_(config)), proxies=proxies)
  return response
def bstack1111ll_opy_(framework):
  return bstack111_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ෼").format(str(framework), __version__) if framework else bstack111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ෽").format(__version__)
def bstack1lll11lll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1111l11l_opy_()
  logger.debug(bstack11l1llll_opy_.format(str(CONFIG)))
  bstack1llll1111_opy_()
  sys.excepthook = bstack1lllll111_opy_
  atexit.register(bstack1l1lll11_opy_)
  signal.signal(signal.SIGINT, bstack11l11l1l_opy_)
  signal.signal(signal.SIGTERM, bstack11l11l1l_opy_)
def bstack1lllll111_opy_(exctype, value, traceback):
  bstack1l1l1ll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
def bstack1l1l1ll1_opy_(message = bstack111_opy_ (u"ࠬ࠭෾")):
  global CONFIG
  try:
    if message:
      bstack111lll11_opy_ = {
        bstack111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ෿"): message
      }
      bstack11l1l1l_opy_(bstack1l11l_opy_, CONFIG, bstack111lll11_opy_)
    else:
      bstack11l1l1l_opy_(bstack1l11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11l1_opy_.format(str(e)))
def bstack1ll11ll1_opy_(bstack1l111lll_opy_, size):
  bstack111ll1ll_opy_ = []
  while len(bstack1l111lll_opy_) > size:
    bstack1111111l_opy_ = bstack1l111lll_opy_[:size]
    bstack111ll1ll_opy_.append(bstack1111111l_opy_)
    bstack1l111lll_opy_   = bstack1l111lll_opy_[size:]
  bstack111ll1ll_opy_.append(bstack1l111lll_opy_)
  return bstack111ll1ll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack11l1ll1l_opy_)
    return
  if sys.argv[1] == bstack111_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ฀")  or sys.argv[1] == bstack111_opy_ (u"ࠨ࠯ࡹࠫก"):
    logger.info(bstack111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩข").format(__version__))
    return
  if sys.argv[1] == bstack111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩฃ"):
    bstack11lllll_opy_()
    return
  args = sys.argv
  bstack1lll11lll_opy_()
  global CONFIG
  global bstack111ll1l_opy_
  global bstack1lll1l1l1_opy_
  global bstack111ll11l_opy_
  global bstack1l1l11ll_opy_
  global bstack1llll111l_opy_
  bstack111lll_opy_ = bstack111_opy_ (u"ࠫࠬค")
  if args[1] == bstack111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬฅ") or args[1] == bstack111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧฆ"):
    bstack111lll_opy_ = bstack111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧง")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧจ"):
    bstack111lll_opy_ = bstack111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨฉ")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩช"):
    bstack111lll_opy_ = bstack111_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪซ")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ฌ"):
    bstack111lll_opy_ = bstack111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧญ")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧฎ"):
    bstack111lll_opy_ = bstack111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨฏ")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩฐ"):
    bstack111lll_opy_ = bstack111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪฑ")
    args = args[2:]
  else:
    if not bstack111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧฒ") in CONFIG or str(CONFIG[bstack111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨณ")]).lower() in [bstack111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ด"), bstack111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨต")]:
      bstack111lll_opy_ = bstack111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨถ")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬท")]).lower() == bstack111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩธ"):
      bstack111lll_opy_ = bstack111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪน")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨบ")]).lower() == bstack111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬป"):
      bstack111lll_opy_ = bstack111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ผ")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫฝ")]).lower() == bstack111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩพ"):
      bstack111lll_opy_ = bstack111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪฟ")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧภ")]).lower() == bstack111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬม"):
      bstack111lll_opy_ = bstack111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ย")
      args = args[1:]
    else:
      os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩร")] = bstack111lll_opy_
      bstack1ll1llll1_opy_(bstack1l1l1l1l_opy_)
  try:
    os.environ[bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪฤ")] = bstack111lll_opy_
    bstack11l1l1l_opy_(bstack1lll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11l1_opy_.format(str(e)))
  global bstack1lllll11l_opy_
  global bstack1ll111ll_opy_
  global bstack111l1l11_opy_
  global bstack1l1ll1ll_opy_
  global bstack1lllll11_opy_
  global bstack11ll1ll1_opy_
  global bstack1ll11l11l_opy_
  global bstack1111llll_opy_
  global bstack1ll11l111_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l11ll1l_opy_
  global bstack1l1111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1l1111_opy_(e, bstack1llll11ll_opy_)
  bstack1lllll11l_opy_ = webdriver.Remote.__init__
  bstack1111llll_opy_ = WebDriver.close
  bstack1l11ll1l_opy_ = WebDriver.get
  if bstack1lll1llll_opy_():
    if bstack1ll1l1ll_opy_() < version.parse(bstack111l1_opy_):
      logger.error(bstack111llll_opy_.format(bstack1ll1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1111l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l1l11_opy_.format(str(e)))
  if (bstack111lll_opy_ in [bstack111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨล"), bstack111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩฦ"), bstack111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬว")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1l1111_opy_(e, bstack1ll1ll1l_opy_)
    bstack1ll111ll_opy_ = Output.end_test
    bstack111l1l11_opy_ = TestStatus.__init__
    bstack1l1ll1ll_opy_ = WebDriverCreator._get_ff_profile
    bstack1lllll11_opy_ = pabot._run
    bstack11ll1ll1_opy_ = QueueItem.__init__
    bstack1ll11l11l_opy_ = pabot._create_command_for_execution
  if bstack111lll_opy_ == bstack111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬศ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1111_opy_(e, bstack11l111l1_opy_)
    bstack1ll11l111_opy_ = Runner.run_hook
    bstack1ll1l11l1_opy_ = Step.run
  if bstack111lll_opy_ == bstack111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ษ"):
    bstack1l1ll1l1_opy_()
    bstack1ll1l1l1l_opy_()
    if bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪส") in CONFIG:
      bstack1lll1l1l1_opy_ = True
      bstack1l1llll1_opy_ = []
      for index, platform in enumerate(CONFIG[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫห")]):
        bstack1l1llll1_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1ll11l1l1_opy_, args=(args[0], index)))
      for t in bstack1l1llll1_opy_:
        t.start()
      for t in bstack1l1llll1_opy_:
        t.join()
    else:
      bstack1l11l11l_opy_(bstack11l1l_opy_)
      exec(open(args[0]).read())
  elif bstack111lll_opy_ == bstack111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨฬ") or bstack111lll_opy_ == bstack111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩอ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1111_opy_(e, bstack1ll1ll1l_opy_)
    bstack1l1ll1l1_opy_()
    bstack1l11l11l_opy_(bstack1lllll_opy_)
    if bstack111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩฮ") in args:
      i = args.index(bstack111_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฯ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack111ll1l_opy_))
    args.insert(0, str(bstack111_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫะ")))
    pabot.main(args)
  elif bstack111lll_opy_ == bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨั"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1111_opy_(e, bstack1ll1ll1l_opy_)
    for a in args:
      if bstack111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧา") in a:
        bstack111ll11l_opy_ = int(a.split(bstack111_opy_ (u"ࠩ࠽ࠫำ"))[1])
      if bstack111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧิ") in a:
        bstack1l1l11ll_opy_ = str(a.split(bstack111_opy_ (u"ࠫ࠿࠭ี"))[1])
      if bstack111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡕࡎࡇࡋࡊࡊࡎࡒࡅࠨึ") in a:
        bstack1llll111l_opy_ = str(a.split(bstack111_opy_ (u"࠭࠺ࠨื"))[1])
    bstack1l11l11l_opy_(bstack1lllll_opy_)
    run_cli(args)
  elif bstack111lll_opy_ == bstack111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺุࠧ"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack1111ll1_opy_ = importlib.find_loader(bstack111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ูࠪ"))
      if bstack1111ll1_opy_ is None:
        bstack1l1111_opy_(e, bstack1llllllll_opy_)
    except Exception as e:
      bstack1l1111_opy_(e, bstack1llllllll_opy_)
    bstack1l1ll1l1_opy_()
    try:
      if bstack111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵฺࠫ") in args:
        i = args.index(bstack111_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ฻"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ฼") in args:
        i = args.index(bstack111_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭฽"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"࠭࠭࡯ࠩ฾") in args:
        i = args.index(bstack111_opy_ (u"ࠧ࠮ࡰࠪ฿"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1ll1l11l_opy_ = config.args
    bstack1l111l_opy_ = config.invocation_params.args
    bstack1l111l_opy_ = list(bstack1l111l_opy_)
    bstack11ll11ll_opy_ = []
    for arg in bstack1l111l_opy_:
      for spec in bstack1ll1l11l_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack11ll11ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack111_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩเ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll1l1ll_opy_)))
                    for bstack1lll1l1ll_opy_ in bstack1ll1l11l_opy_]
    bstack11ll11ll_opy_.append(bstack111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫแ"))
    bstack11ll11ll_opy_.append(bstack111_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩโ"))
    bstack1l1l1111_opy_ = []
    for spec in bstack1ll1l11l_opy_:
      bstack1l111l1l_opy_ = []
      bstack1l111l1l_opy_.append(spec)
      bstack1l111l1l_opy_ += bstack11ll11ll_opy_
      bstack1l1l1111_opy_.append(bstack1l111l1l_opy_)
    bstack1lll1l1l1_opy_ = True
    bstack1llll111_opy_ = 1
    if bstack111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫใ") in CONFIG:
      bstack1llll111_opy_ = CONFIG[bstack111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬไ")]
    bstack1ll1lllll_opy_ = int(bstack1llll111_opy_)*int(len(CONFIG[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩๅ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪๆ")]):
      for bstack1l111l1l_opy_ in bstack1l1l1111_opy_:
        item = {}
        item[bstack111_opy_ (u"ࠨࡣࡵ࡫ࠬ็")] = bstack1l111l1l_opy_
        item[bstack111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ่")] = index
        execution_items.append(item)
    bstack1lll111_opy_ = bstack1ll11ll1_opy_(execution_items, bstack1ll1lllll_opy_)
    for execution_item in bstack1lll111_opy_:
      bstack1l1llll1_opy_ = []
      for item in execution_item:
        bstack1l1llll1_opy_.append(threading.Thread(name=str(item[bstack111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹ้ࠩ")]),
                                            target=bstack1l11l111_opy_,
                                            args=(item[bstack111_opy_ (u"ࠫࡦࡸࡧࠨ๊")],)))
      for t in bstack1l1llll1_opy_:
        t.start()
      for t in bstack1l1llll1_opy_:
        t.join()
  elif bstack111lll_opy_ == bstack111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩ๋ࠬ"):
    try:
      from behave.__main__ import main as bstack11lll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1111_opy_(e, bstack11l111l1_opy_)
    bstack1l1ll1l1_opy_()
    bstack1lll1l1l1_opy_ = True
    bstack1llll111_opy_ = 1
    if bstack111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭์") in CONFIG:
      bstack1llll111_opy_ = CONFIG[bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧํ")]
    bstack1ll1lllll_opy_ = int(bstack1llll111_opy_)*int(len(CONFIG[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๎")]))
    config = Configuration(args)
    bstack1ll1l11l_opy_ = config.paths
    bstack1l1ll11l_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1ll1l11l_opy_:
        bstack1l1ll11l_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack111_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ๏"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1lll1l1ll_opy_)))
                    for bstack1lll1l1ll_opy_ in bstack1ll1l11l_opy_]
    bstack1l1l1111_opy_ = []
    for spec in bstack1ll1l11l_opy_:
      bstack1l111l1l_opy_ = []
      bstack1l111l1l_opy_ += bstack1l1ll11l_opy_
      bstack1l111l1l_opy_.append(spec)
      bstack1l1l1111_opy_.append(bstack1l111l1l_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๐")]):
      for bstack1l111l1l_opy_ in bstack1l1l1111_opy_:
        item = {}
        item[bstack111_opy_ (u"ࠫࡦࡸࡧࠨ๑")] = bstack111_opy_ (u"ࠬࠦࠧ๒").join(bstack1l111l1l_opy_)
        item[bstack111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ๓")] = index
        execution_items.append(item)
    bstack1lll111_opy_ = bstack1ll11ll1_opy_(execution_items, bstack1ll1lllll_opy_)
    for execution_item in bstack1lll111_opy_:
      bstack1l1llll1_opy_ = []
      for item in execution_item:
        bstack1l1llll1_opy_.append(threading.Thread(name=str(item[bstack111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭๔")]),
                                            target=bstack11llll11_opy_,
                                            args=(item[bstack111_opy_ (u"ࠨࡣࡵ࡫ࠬ๕")],)))
      for t in bstack1l1llll1_opy_:
        t.start()
      for t in bstack1l1llll1_opy_:
        t.join()
  else:
    bstack1ll1llll1_opy_(bstack1l1l1l1l_opy_)
  bstack1lllll1_opy_()
def bstack1lllll1_opy_():
  global CONFIG
  try:
    if bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๖") in CONFIG:
      host = bstack111_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭๗") if bstack111_opy_ (u"ࠫࡦࡶࡰࠨ๘") in CONFIG else bstack111_opy_ (u"ࠬࡧࡰࡪࠩ๙")
      user = CONFIG[bstack111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ๚")]
      key = CONFIG[bstack111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ๛")]
      bstack1111l1l1_opy_ = bstack111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ๜") if bstack111_opy_ (u"ࠩࡤࡴࡵ࠭๝") in CONFIG else bstack111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ๞")
      url = bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ๟").format(user, key, host, bstack1111l1l1_opy_)
      headers = {
        bstack111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ๠"): bstack111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ๡"),
      }
      if bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๢") in CONFIG:
        params = {bstack111_opy_ (u"ࠨࡰࡤࡱࡪ࠭๣"):CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๤")], bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๥"):CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๦")]}
      else:
        params = {bstack111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๧"):CONFIG[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๨")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1lll11l1l_opy_ = response.json()[0][bstack111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ๩")]
        if bstack1lll11l1l_opy_:
          bstack1ll1l111_opy_ = bstack1lll11l1l_opy_[bstack111_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ๪")].split(bstack111_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨ๫"))[0] + bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫ๬") + bstack1lll11l1l_opy_[bstack111_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ๭")]
          logger.info(bstack11111l_opy_.format(bstack1ll1l111_opy_))
          bstack111l11l_opy_ = CONFIG[bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๮")]
          if bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๯") in CONFIG:
            bstack111l11l_opy_ += bstack111_opy_ (u"ࠧࠡࠩ๰") + CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๱")]
          if bstack111l11l_opy_!= bstack1lll11l1l_opy_[bstack111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๲")]:
            logger.debug(bstack111l11ll_opy_.format(bstack1lll11l1l_opy_[bstack111_opy_ (u"ࠪࡲࡦࡳࡥࠨ๳")], bstack111l11l_opy_))
    else:
      logger.warn(bstack1l1ll111_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lll11_opy_.format(str(e)))
def bstack1lll1ll1l_opy_(url):
  global CONFIG
  global bstack11l1lll1_opy_
  if not bstack11l1lll1_opy_:
    hostname = bstack11ll1l1_opy_(url)
    is_private = bstack1l11l1ll_opy_(hostname)
    if not bstack1l1l111_opy_(CONFIG) and is_private:
      bstack11l1lll1_opy_ = hostname
def bstack11ll1l1_opy_(url):
  return urlparse(url).hostname
def bstack1l11l1ll_opy_(hostname):
  for bstack1l1lll111_opy_ in bstack1l1l1l_opy_:
    regex = re.compile(bstack1l1lll111_opy_)
    if regex.match(hostname):
      return True
  return False