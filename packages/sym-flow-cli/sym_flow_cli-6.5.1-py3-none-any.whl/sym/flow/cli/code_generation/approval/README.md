# Overview
Welcome to Sym! 

Sym helps you code your way out of messy access management problems with approval workflows built in
Python and Terraform. Run these Sym Flows in Slack for seamless access management across all of your teams.

In this directory, you will find a set of files that will be used to configure your first Sym Flow.

- `main.tf`: The main Terraform file containing all of your Sym resource declarations
- `impl.py`: A sample implementation file that customizes the example Sym Flow to send request messages to the `#sym-requests` Slack channel
- `versions.tf`: A file declaring the Sym Terraform provider version

If you have any questions or feedback, please reach out to us at support@symops.com.

# Helpful Links
- [Sym Docs](https://docs.symops.com/)
- [Sym Terraform Provider Docs](https://registry.terraform.io/providers/symopsio/sym/latest/docs)
- [Sym Implementation Examples](https://github.com/symopsio/examples)

# Configuration Details
## main.tf
This file contains the Terraform configurations for all the Sym resources needed to implement a basic Sym Flow that
consists of three steps:
1. Prompt - Sym asks the user to fill in a form with fields defined in the `sym_flow` resource (described below)
2. Request - Sym takes the values inputted by the user in the Prompt step and posts the request to `#sym-requests`
3. Approve/Deny - The request is approved or denied by someone in Slack via buttons

This type of Flow is called an "Approval-Only Flow". Read more about Approval-Only Flows in our [docs](https://docs.symops.com/docs/approval-only-flows).

### [sym_flow](https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/flow)
The `sym_flow` resource defines the Flow that a user will run in Slack. This example configuration contains:
- `name`: A unique, human-readable identifier for the Flow.
- `label`: The display name for the Flow. This is what you'll see in Slack.	
- `implementation`: The path to a file where the Sym Python SDK will be used to customize the workflow. In this case, `impl.py`
- `environment_id`: The Environment this Flow belongs to (e.g. `prod`, `staging`, `sandbox`). See `sym_environment` below. 
- `params`: A Terraform block containing parameters to customize this Flow's behavior.
  - `prompt_field`: Terraform blocks describing what inputs to show users when this Flow is run.

### [sym_environment](https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/environment)
The `sym_environment` resource is a collection of shared configuration for your Flows. 
For example, it will tell your Flow where to send errors and which integrations to use.

In this example, we have named the environment `main` (according to a local variable), and have configured
an Error Logger to capture any errors that occur when running Flows in this Environment. Finally, there is
a single integration with Slack that tells Sym which Slack workspace to send the requests to.

### [sym_integration](https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/integration)
`sym_integration` resources allow you to provide Sym with the credentials and context to connect to an external service.
In this case, the Slack integration only needs your Workspace ID.

### [sym_error_logger](https://registry.terraform.io/providers/symopsio/sym/latest/docs/resources/error_logger)
The `sym_error_logger` resource configures a channel in Slack as the destination for any warnings and errors that occur during
the execution of a Flow. In this example, we have configured it to send messages to the `#sym-errors` channel. **Make sure
that you create this channel in your workspace! Otherwise, the messages will not be delivered.**

## impl.py
The `impl.py` file is a Python file that allows you to customize your Flow's logic in Python. This is where you may
implement any number of [Hooks and Reducers](https://docs.symops.com/docs/workflow-handlers). 
- Reducers are prefixed with `get_`, and return a single value.
- Hooks are prefixed with `on_` or `after_`, and allow you to alter control flow by inserting custom logic before or after an Event is processed.

In this example, the `impl.py` file implements a single Reducer `get_approvers`, which tells Sym where to send
requests in Slack. This example returns the channel `#sym-requests`, and allows requesters
to approve their own requests (`allow_self=True`).

While the `get_approvers` Reducer is the only required part of an `impl.py`, there are many [Hooks](https://docs.symops.com/docs/hooks)
that you may implement to customize your Flow's logic. For example, you might want to implement an 
[`on_request` Hook](https://docs.symops.com/docs/hooks#on_request) that auto-approves users that are on-call on PagerDuty.
