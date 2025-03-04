from slither import Slither
from slither.detectors import AbstractDetector, DetectorClassification

class ReentrancyDetector(AbstractDetector):
    ARGUMENT = "reentrancy-custom"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM
    HELP = "Custom reentrancy detector"

    def _detect(self):
        results = []
        for contract in self.slither.contracts:
            for func in contract.functions:
                if func.can_reenter():
                    info = f"⚠️ Reentrancy in {contract.name}.{func.name}\n"
                    json = self.generate_result(info)
                    results.append(json)
        return results

if __name__ == "__main__":
    slither = Slither("contracts/ReentrancyDemo.sol")
    slither.register_detector(ReentrancyDetector)
    slither.run_detectors()
