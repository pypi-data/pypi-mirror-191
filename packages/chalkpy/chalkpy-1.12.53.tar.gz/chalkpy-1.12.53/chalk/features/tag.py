from typing import List, Tuple, Union

from typing_extensions import TypeAlias

Tags: TypeAlias = Union[List[str], Tuple[str, ...], str]
"""
Tags allow you to scope requests within an
environment. Both tags and environment need
to match for a resolver to be a candidate to
execute.

Like Environments, tags control when resolvers
run based on the Online Context or Training Context
matching the tags provided to the resolver decorator.
Resolvers optionally take a keyword argument named
tags that can take one of three types:
- `None` (default) - The resolver will be a candidate to run for every set of tags.
- `str` - The resolver will run only if this tag is provided.
- `list[str]` - The resolver will run in all of the specified tags match.

See more at https://docs.chalk.ai/docs/resolver-tags
"""

Environments: TypeAlias = Union[List[str], Tuple[str, ...], str]
"""
Environments are used to trigger behavior
in different deployments such as staging,
production, and local development.
For example, you may wish to interact with
a vendor via an API call in the production
environment, and opt to return a constant
value in a staging environment.

`Environments` can take one of three types:
  - `None` (default) - candidate to run in every environment
  - `str` - run only in this environment
  - `list[str]` - run in any of the specified environment and no others

See more at https://docs.chalk.ai/docs/resolver-environments
"""
