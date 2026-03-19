class ReportService:

    def generate(self, before, after):
        return {
            "input": len(before),
            "output": len(after),
            "duplicates_removed": len(before) - len(after),
            "completeness": after.notnull().mean().to_dict()
        }