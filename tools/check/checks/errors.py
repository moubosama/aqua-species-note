"""確認のプログラムで使う例外。

site.py は読み込むときに site/i18n/*.toml を読むので、そこで出た ConfigError を
run_checks.py が受け止められるよう、例外だけをこの小さなモジュールに置く。
（site.py からも ConfigError として読める。）
"""


class ConfigError(Exception):
    """設定ファイルが読めない、または形がおかしいとき。"""
