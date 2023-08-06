import pytest
from t5html import lineparser as lp
from t5html import importer as imp

from os.path import expanduser as _xu

class TestImporterSyntax:
    @pytest.mark.parametrize("tin, tout",
            [("@@ fname from fpath", "fpath/fname"),
             ("@@ fname", _xu("~/.local/share/t5html/fname")),])
    def test_importline(s, tin, tout):
        assert imp.path_from_import_string(tin) == tout

    @pytest.mark.parametrize("tin, tout",
            [(lp.LineStructure(0, "@@ fname from fpath", 'import'), "fpath/fname"),
             (lp.LineStructure(0, "@@ fname", 'import'), _xu("~/.local/share/t5html/fname")),])
    def test_importline_from_LS(s, tin, tout):
        assert imp.path_from_LineStructure(tin) == tout

    def test_batch_pathconversion(s):
        tin = [lp.LineStructure(0, "@@ fname from fpath", 'import'),
               lp.LineStructure(1, "@@ fname", 'import'), ]
        tout = [ "fpath/fname", _xu("~/.local/share/t5html/fname")]
        assert tout == imp.list_of_imports(tin)

    def test_for_existing_fileimports(s):
        # /etc/hosts should be avaiable under all *nix sysstems
        tin = [ "fpath/fname", _xu("~/.local/share/t5html/fname"), "/etc/hosts"]
        tout = ["/etc/hosts"]
        assert tout == imp.existing_imports(tin)

# vi: set et ts=4 ts=4 ai cc=78 nowrap nu so=5:
