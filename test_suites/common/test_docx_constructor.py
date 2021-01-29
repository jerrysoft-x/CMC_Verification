import os
import shutil

import pytest

# This test file is used to test DocxFile class
# Prepare the test: three files, a docx file which is mostly expected, a doc file which should be converted to docx,
# and a file whose extension name is neither docx nor doc.


# If the extension of the passed file path is neither docx nor doc, a ValueError is expected.
from common import DocxFile


def test_invalid_file_path():
    file_path = 'invalid_file_path.ext'
    abs_path = os.path.abspath(file_path)
    with pytest.raises(ValueError) as excinfo:
        with DocxFile(file_path):
            pass
    expected_error_message = (
        f"The extension name of file path {abs_path} passed to DocxFile constructor is neither docx nor doc."
    )
    assert str(excinfo.value) == expected_error_message


@pytest.fixture
def doc_file_sample():
    # Prepare the environment
    test_file = 'DNVGL质保书样本.doc'
    abs_path = os.path.abspath(test_file)
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(f"{test_file}x"):
        os.remove(f"{test_file}x")
    file_source = os.path.abspath(r"../test_data")
    shutil.copy(os.path.join(file_source, test_file), test_file)
    return abs_path


# Test open up doc file.
def test_doc_file_path(doc_file_sample):
    # If the file extension is doc, the DocxFile constructor will create an equivalent in docx format, and the doc file
    # will be removed. The file path of the docx file object should be updated as well.
    with DocxFile(doc_file_sample) as docx_file:
        assert os.path.exists(f"{doc_file_sample}x")
        assert not os.path.exists(doc_file_sample)
        assert isinstance(docx_file, DocxFile)
        assert docx_file.file_path == f"{doc_file_sample}x"
        assert len(docx_file.document.tables) > 0
        assert len(docx_file.document.paragraphs) > 0
        assert docx_file.steel_plant is not None
        assert docx_file.steel_plant == 'CHANGSHU LONGTENG SPECIAL STEEL CO., LTD.'


@pytest.fixture
def docx_file_sample():
    test_file = 'DNVGL质保书样本.docx'
    abs_path = os.path.abspath(test_file)
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(f"{test_file}x"):
        os.remove(f"{test_file}x")
    file_source = os.path.abspath(r"../test_data")
    shutil.copy(os.path.join(file_source, test_file), test_file)
    return abs_path


# Test open up doc file.
def test_docx_file_path(docx_file_sample):
    with DocxFile(docx_file_sample) as docx_file:
        assert os.path.exists(docx_file_sample)
        assert isinstance(docx_file, DocxFile)
        assert docx_file.file_path == docx_file_sample
        assert len(docx_file.document.tables) == 6
        assert len(docx_file.document.paragraphs) == 6 * 3
        assert docx_file.steel_plant is not None
        assert docx_file.steel_plant == 'CHANGSHU LONGTENG SPECIAL STEEL CO., LTD.'
