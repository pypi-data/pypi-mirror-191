import random

from joye.oss import list_folder_data, open_data, open_strategy


def test_data_write_and_read():
    content = f"test{random.random()}".encode("utf-8")
    with open_data("test.data", "wb") as f:
        f.write(content)

    with open_data("test.data", "rb") as f:
        data = f.read()
        assert data == content, "data error"

    content = f"test{random.random()}".encode("utf-8")
    with open_strategy("test.data", "wb") as f:
        f.write(content)

    with open_strategy("test.data", "rb") as f:
        data = f.read()
        assert data == content, "data error"

def test_list_data_folder():
    out = list_folder_data("")
    assert "test.data" in out


if __name__ == "__main__":
    # test_data_write_and_read()
    out = list_folder_data("")
    print(out)
