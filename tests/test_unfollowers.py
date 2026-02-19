import json

from python_tools.social.unfollower_checker.core import find_unfollowers


def test_find_unfollowers_from_text(tmp_path):
    following = tmp_path / "following.txt"
    followers = tmp_path / "followers.txt"

    following.write_text("alice\nbob\ncarol\n", encoding="utf-8")
    followers.write_text("alice\ncarol\n", encoding="utf-8")

    assert find_unfollowers(str(following), str(followers)) == ["bob"]


def test_find_unfollowers_from_instagram_json(tmp_path):
    following = tmp_path / "following.json"
    followers = tmp_path / "followers_1.json"

    following_payload = {
        "relationships_following": [
            {
                "string_list_data": [
                    {"value": "alice", "timestamp": 1, "href": "https://instagram.com/alice"}
                ]
            },
            {
                "string_list_data": [
                    {"value": "bob", "timestamp": 1, "href": "https://instagram.com/bob"}
                ]
            },
        ]
    }
    followers_payload = [
        {
            "string_list_data": [
                {"value": "alice", "timestamp": 1, "href": "https://instagram.com/alice"}
            ]
        }
    ]

    following.write_text(json.dumps(following_payload), encoding="utf-8")
    followers.write_text(json.dumps(followers_payload), encoding="utf-8")

    assert find_unfollowers(str(following), str(followers)) == ["bob"]
