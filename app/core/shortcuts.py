import re

ALPHANUMERIC_RE = re.compile(r'[^a-zA-Z0-9]')


def clean_token_asset_name(asset_name: str) -> str:
    """
    :param asset_name: The asset_name segment of a Cardano native token

    Cardano native assets are identified by the concatenation of
    their policy ID and an optional name:
    <asset_id> = <policy_id>.<asset_name>

    The asset name is restricted to alphanumeric characters, so
    use this shortcut to exclude invalid characters.
    """
    return ALPHANUMERIC_RE.sub('', asset_name)
