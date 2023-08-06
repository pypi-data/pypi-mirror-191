import pytest

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
from BdrcDbLib.DbOrm.models.drs import *


@pytest.mark.skip("in production")
def test_gb_ready_track():
    assert False


@pytest.mark.skip("in production")
def test_works():
    assert False


@pytest.mark.skip("in production")
def test_volumes():
    assert False


def test_gb_metadata():
    with DrsDbContextBase() as ctx:
        xx = ctx.session.query(GbMetadata).first()
        print(xx)


@pytest.mark.skip("in production")
def test_gb_content():
    assert False


@pytest.mark.skip("in production")
def test_gb_state():
    assert False


@pytest.mark.skip("in production")
def test_gb_download():
    assert False


@pytest.mark.skip("in production")
def test_gb_ready_track():
    assert False


@pytest.mark.skip("in production")
def test_gb_unpack():
    assert False


@pytest.mark.skip("in production")
def test_gb_distribution():
    assert False


def test_dip_activities():
    with DrsDbContextBase() as ctx:
        dbAx = ctx.session.query(DipActivities).all()
        print(dbAx)
        assert len(dbAx) > 3
        xxx = ctx.session.query(DipActivities.label).all()
        print(xxx)
