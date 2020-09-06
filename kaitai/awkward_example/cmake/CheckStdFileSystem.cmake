include(CheckCXXSourceCompiles)

set(CHECK_STD_FS_TEST_FILE "${CMAKE_CURRENT_LIST_DIR}/CheckStdFileSystem.cpp")
file(READ "${CHECK_STD_FS_TEST_FILE}" CHECK_STD_FS_TEST_FILE_CONTENTS)

function(checkStdFileSystem resultVar)
	check_cxx_source_compiles("${CHECK_STD_FS_TEST_FILE_CONTENTS}" "${resultVar}")
endfunction()