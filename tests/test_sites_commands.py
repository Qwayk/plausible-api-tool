from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from plausible_api_tool.commands.sites import (
    cmd_site_custom_props_list,
    cmd_site_create,
    cmd_site_delete,
    cmd_site_get,
    cmd_site_goals_list,
    cmd_site_guests_list,
    cmd_site_list,
    cmd_site_teams_list,
)
from plausible_api_tool.output import Output


class _Audit:
    def write(self, *_args, **_kwargs) -> None:
        return


class TestSitesCommands(unittest.TestCase):
    def _ctx(self, **overrides):
        base = {
            "cfg": SimpleNamespace(site_id="example.com", base_url="https://plausible.local"),
            "http": None,
            "out": Output(mode="json"),
            "audit": _Audit(),
            "apply": False,
            "yes": False,
            "ack_irreversible": False,
            "plan_out": None,
            "receipt_out": None,
        }
        base.update(overrides)
        return base

    def test_site_list_calls_client(self) -> None:
        args = SimpleNamespace(after=None, before=None, limit=100, team_id=None)
        ctx = self._ctx()

        captured = {}

        def fake_list(_self, **kwargs):
            captured.update(kwargs)
            return {"sites": []}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.sites_list", new=fake_list):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_list(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertIn("response", payload)
        self.assertEqual(captured.get("limit"), 100)

    def test_site_get_defaults_site_id(self) -> None:
        args = SimpleNamespace(site_id=None)
        ctx = self._ctx()

        captured = {}

        def fake_get(_self, site_id):
            captured["site_id"] = site_id
            return {"domain": site_id}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_get", new=fake_get):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_get(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertEqual(captured["site_id"], "example.com")
        self.assertEqual(payload["site_id"], "example.com")

    def test_site_teams_list_calls_client(self) -> None:
        ctx = self._ctx()

        with patch("plausible_api_tool.commands.sites.PlausibleClient.sites_teams_list", return_value={"teams": []}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_teams_list(SimpleNamespace(), ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])

    def test_site_goals_list_defaults_site_id(self) -> None:
        args = SimpleNamespace(site_id=None, after=None, before=None, limit=100)
        ctx = self._ctx()

        captured = {}

        def fake_goals_list(_self, *, site_id, after=None, before=None, limit=None):
            captured["site_id"] = site_id
            captured["limit"] = limit
            return {"goals": []}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_goals_list", new=fake_goals_list):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_goals_list(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertEqual(captured["site_id"], "example.com")
        self.assertEqual(captured["limit"], 100)
        self.assertEqual(payload["site_id"], "example.com")

    def test_site_custom_props_list_defaults_site_id(self) -> None:
        args = SimpleNamespace(site_id=None)
        ctx = self._ctx()

        captured = {}

        def fake_list(_self, *, site_id):
            captured["site_id"] = site_id
            return {"custom_properties": []}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_custom_props_list", new=fake_list):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_custom_props_list(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertEqual(captured["site_id"], "example.com")
        self.assertEqual(payload["site_id"], "example.com")

    def test_site_guests_list_defaults_site_id(self) -> None:
        args = SimpleNamespace(site_id=None, after=None, before=None, limit=100)
        ctx = self._ctx()

        captured = {}

        def fake_list(_self, *, site_id, after=None, before=None, limit=None):
            captured["site_id"] = site_id
            captured["limit"] = limit
            return {"guests": []}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_guests_list", new=fake_list):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_guests_list(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertEqual(captured["site_id"], "example.com")
        self.assertEqual(captured["limit"], 100)
        self.assertEqual(payload["site_id"], "example.com")

    def test_site_create_dry_run_refuses_without_apply(self) -> None:
        args = SimpleNamespace(domain="test-domain.com", timezone=None, team_id=None, tracker_config=None, tracker_config_file=None)
        ctx = self._ctx(apply=False, yes=False)

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_create") as p_create:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cmd_site_create(args, ctx)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["dry_run"])
        self.assertTrue(payload["refused"])
        self.assertIn("plan", payload)
        p_create.assert_not_called()

    def test_site_create_apply_requires_yes(self) -> None:
        args = SimpleNamespace(domain="test-domain.com", timezone=None, team_id=None, tracker_config=None, tracker_config_file=None)
        ctx = self._ctx(apply=True, yes=False)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_site_create(args, ctx)
        self.assertEqual(rc, 1)
        payload = json.loads(buf.getvalue())
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_type"], "SafetyError")

    def test_site_delete_apply_requires_ack_irreversible(self) -> None:
        args = SimpleNamespace(site_id="test-domain.com")
        ctx = self._ctx(apply=True, yes=True, ack_irreversible=False)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cmd_site_delete(args, ctx)
        self.assertEqual(rc, 1)
        payload = json.loads(buf.getvalue())
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error_type"], "SafetyError")

    def test_site_create_plan_and_receipt_out_write_files(self) -> None:
        args = SimpleNamespace(domain="test-domain.com", timezone=None, team_id=None, tracker_config=None, tracker_config_file=None)
        with tempfile.TemporaryDirectory() as d:
            plan_path = str(Path(d) / "plan.json")
            receipt_path = str(Path(d) / "receipt.json")
            ctx = self._ctx(apply=True, yes=True, ack_irreversible=False, plan_out=plan_path, receipt_out=receipt_path)

            with patch("plausible_api_tool.commands.sites.PlausibleClient.site_create", return_value={"domain": "test-domain.com"}):
                with patch("plausible_api_tool.commands.sites.PlausibleClient.site_get", return_value={"domain": "test-domain.com"}):
                    buf = io.StringIO()
                    with redirect_stdout(buf):
                        rc = cmd_site_create(args, ctx)
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertTrue(payload["ok"])
            self.assertTrue(Path(plan_path).exists())
            self.assertTrue(Path(receipt_path).exists())
            plan_obj = json.loads(Path(plan_path).read_text(encoding="utf-8"))
            receipt_obj = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
            self.assertEqual(plan_obj["tool"], "plausible-api-tool")
            self.assertEqual(receipt_obj["tool"], "plausible-api-tool")
            self.assertNotIn("api_key", json.dumps(plan_obj))
            self.assertNotIn("api_key", json.dumps(receipt_obj))

    def test_site_create_calls_read_back_get(self) -> None:
        args = SimpleNamespace(domain="test-domain.com", timezone=None, team_id=None, tracker_config=None, tracker_config_file=None)
        ctx = self._ctx(apply=True, yes=True)

        calls = {"get": 0}

        def fake_get(_self, site_id):
            calls["get"] += 1
            return {"domain": site_id}

        with patch("plausible_api_tool.commands.sites.PlausibleClient.site_create", return_value={"domain": "test-domain.com"}):
            with patch("plausible_api_tool.commands.sites.PlausibleClient.site_get", new=fake_get):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = cmd_site_create(args, ctx)
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(calls["get"], 1)
