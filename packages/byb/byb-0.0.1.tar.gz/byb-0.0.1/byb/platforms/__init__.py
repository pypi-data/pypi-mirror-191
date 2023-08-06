from byb.platforms.instagram import InstagramPost

PLATFORMS = {InstagramPost().name: InstagramPost}


def get_platform(platform: str):
    """Fetch a platform object given a string.

    Args:
        platform (str): A `Platform` from the global `PLATFORMS` list.

    Raises:
        ValueError: Thrown if a missing/invalid platform is passed in.

    Returns:
        Platform: The associated `Platform`.
    """
    if platform not in PLATFORMS:
        raise ValueError(
            f"Invalid platform: '{platform}'. Choose from {', '.join([str(k) for k in PLATFORMS.keys()])}"
        )
    return PLATFORMS.get(platform)
