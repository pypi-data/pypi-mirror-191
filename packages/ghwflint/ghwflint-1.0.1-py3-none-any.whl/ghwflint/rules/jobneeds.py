from ghwflint.rules.validator import ValidationRule, ValidationContext


class ValidationRuleJobNeeds(ValidationRule):
    def validate(self, context: ValidationContext):
        """
        Validates that each job's needs section only references other jobs defined earlier in the workflow.
        :param context:
        """
        workflow = context.workflow
        jobs = workflow.get("jobs", {})
        job_ids = list(jobs.keys())
        for job_id in job_ids:
            job = jobs[job_id]
            needs = job.get("needs", [])
            if not isinstance(needs, list):
                needs = [needs]
            for need in needs:
                if need not in job_ids:
                    context.error(job, "needs", f"job '{job_id}' needs '{need}', but '{need}' is not defined.")
                if need == job_id:
                    context.error(job, "needs", f"job '{job_id}' needs '{need}', but '{need}' is the same job.")
