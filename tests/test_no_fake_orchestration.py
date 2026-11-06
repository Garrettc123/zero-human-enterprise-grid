"""Zero-Human Grid must not fabricate repository creation, deployment or MRR."""
import asyncio
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "orchestrator" / "autonomous_orchestrator.py"


class NoFakeOrchestration(unittest.TestCase):
    def test_source_never_returns_fake_success(self):
        src = MODULE.read_text()
        self.assertNotIn('"created": True', src)
        self.assertNotIn('return True\n', src)
        self.assertNotIn('demo_token', src)

    def test_plans_are_not_deployments_or_earnings(self):
        import sys
        spec = importlib.util.spec_from_file_location("autonomous_orchestrator", MODULE)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        orchestrator = mod.AutonomousOrchestrator("")
        product = asyncio.run(orchestrator.create_product_line("mesh-messenger"))
        self.assertEqual(product.status, "planned")
        self.assertIsNone(orchestrator.get_portfolio_summary()["total_mrr"])
        self.assertFalse(asyncio.run(orchestrator.deploy_product_line(product.name)))
        self.assertEqual(product.status, "not_deployed")
        with self.assertRaises(RuntimeError):
            asyncio.run(orchestrator.github_manager.create_repository(product))


if __name__ == "__main__":
    unittest.main()
