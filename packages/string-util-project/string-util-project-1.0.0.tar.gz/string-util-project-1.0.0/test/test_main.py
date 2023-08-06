from src.package.main import convert_to_bold


def test_convert_to_bold():
    """Test the result of the convert_to_bold method"""
    assert convert_to_bold("Crest Data Systems") == "𝐂𝐫𝐞𝐬𝐭 𝐃𝐚𝐭𝐚 𝐒𝐲𝐬𝐭𝐞𝐦𝐬"
