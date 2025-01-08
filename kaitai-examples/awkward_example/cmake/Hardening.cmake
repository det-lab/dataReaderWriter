#This is free and unencumbered software released into the public domain.
#Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.
#In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#For more information, please refer to <https://unlicense.org/>

include(CheckCXXCompilerFlag)

function(determineSupportedHardeningFlags property)
	set(FLAGS_HARDENING "")
	foreach(flag ${ARGN})
		unset(var_name)
		string(REPLACE "=" "_eq_" var_name ${flag})
		string(REPLACE "," "_comma_" var_name ${var_name})
		set(var_name "SUPPORTS_HARDENING_${property}_${var_name}")
		check_cxx_compiler_flag(${flag} ${var_name})#since linker flags and other flags are in the form of compiler flags
		if(${${var_name}})
			list(APPEND FLAGS_HARDENING "${flag}")
		endif()
	endforeach(flag)
	list(JOIN FLAGS_HARDENING " " FLAGS_HARDENING)
	message(STATUS "FLAGS_HARDENING ${FLAGS_HARDENING}")
	set(HARDENING_${property} "${FLAGS_HARDENING}" CACHE STRING "Hardening flags")
endfunction(determineSupportedHardeningFlags)

function(processFlagsList target property)
	get_target_property(FLAGS_UNHARDENED ${target} ${property})
	if(FLAGS_UNHARDENED MATCHES "FLAGS_UNHARDENED-NOTFOUND")
		set(FLAGS_UNHARDENED "")
	endif()
	message(STATUS "processFlagsList ${target} ${property} ${FLAGS_UNHARDENED}")
	message(STATUS "HARDENING_${property} ${HARDENING_${property}}")
	if(HARDENING_${property})
	else()
		determineSupportedHardeningFlags(${property} ${ARGN})
	endif()
	
	set(FLAGS_HARDENED ${FLAGS_UNHARDENED})
	list(APPEND FLAGS_HARDENED ${HARDENING_${property}})
	list(JOIN FLAGS_HARDENED " " FLAGS_HARDENED)
	message(STATUS "${target} PROPERTIES ${property} ${FLAGS_HARDENED}")
	set_target_properties(${target} PROPERTIES ${property} "${FLAGS_HARDENED}")
endfunction(processFlagsList)

function(setupPIC target)
	set_property(TARGET ${target} PROPERTY POSITION_INDEPENDENT_CODE ON) # FUCK, doesn't work
	if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
		get_target_property(type ${target} TYPE)
		if(type STREQUAL "EXECUTABLE")
			list(APPEND HARDENING_COMPILER_FLAGS
				"-fPIE"
			)
		else()
			list(APPEND HARDENING_COMPILER_FLAGS
				"-fPIC"
			)
		endif()
		list(APPEND HARDENING_LINKER_FLAGS
			"-pie"
		)
	elseif(MSVC)
		list(APPEND HARDENING_COMPILER_FLAGS
			"/dynamicbase" "/HIGHENTROPYVA"
		)
	else()
		message(ERROR "The compiler is not supported")
	endif()
endfunction(setupPIC)

function(harden target)
	setupPIC("${target}")
	if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
		list(APPEND HARDENING_COMPILER_FLAGS
			"-Wall" "-Wextra" "-Wconversion" "-Wformat" "-Wformat-security" "-Werror=format-security"
			"-fno-strict-aliasing" "-mmitigate-rop" "-fno-common"
			#"-fstack-check"
			"-fstack-clash-protection"
			"-mcet"
			"-fsanitize=cfi"
			"-fsanitize=cfi-cast-strict"
			"-fsanitize=cfi-derived-cast"
			"-fsanitize=cfi-unrelated-cast"
			"-fsanitize=cfi-nvcall"
			"-fsanitize=cfi-vcall"
			"-fsanitize=cfi-icall"
			"-fsanitize=cfi-mfcall"
			"-mindirect-branch"
			"-mindirect-branch=thunk-extern"
			"-mindirect-branch=thunk-inline"
			"-mindirect-return"
			"-mindirect-branch-register"
			"-mindirect-branch-loop"
			"-mno-indirect-branch-register"
		)
		list(APPEND HARDENING_LINKER_FLAGS
			"-Wl,-O1"
			"-Wl,--sort-common"
			"-Wl,--as-needed"
			"-Wl,-flto"
		)
		if(CMAKE_SYSTEM_NAME MATCHES "Windows")
			list(APPEND HARDENING_LINKER_FLAGS
				"-Wl,--export-all-symbols"
				"-Wl,--nxcompat"
				"-Wl,--dynamicbase"
			)
			if(CMAKE_SIZEOF_VOID_P EQUAL 8)
			#	list(APPEND HARDENING_LINKER_FLAGS "-Wl,--image-base,0x140000000") # doesn't work for this project
			endif()
		elseif(CMAKE_SYSTEM_NAME MATCHES "Linux") # other using ELF too?
			list(APPEND HARDENING_COMPILER_FLAGS
				# on MinGW hello world works, but more complex things just exit without any output or crash in the middle of execution
				"-fstack-protector"
				"-fstack-protector-strong"
			)
			list(APPEND HARDENING_LINKER_FLAGS
				# not present in MinGW
				"-Wl,-z,relro"
				"-Wl,-z,now"
				"-Wl,-z,ibtplt"
				"-Wl,-z,ibt"
				"-Wl,-z,shstk"
			)
		endif()
		set(HARDENING_MACRODEFS
			"-D_FORTIFY_SOURCE=2"
		)
	elseif(MSVC)
		set(HARDENING_COMPILER_FLAGS "/sdl" "/GS" "/SafeSEH" "/guard:cf" "/HIGHENTROPYVA")
		set(HARDENING_LINKER_FLAGS "/guard:cf")
	else()
		message(ERROR "The compiler is not supported")
	endif()

	processFlagsList(${target} COMPILE_FLAGS ${HARDENING_COMPILER_FLAGS})
	processFlagsList(${target} LINK_FLAGS ${HARDENING_LINKER_FLAGS})
	target_compile_definitions(${target} PRIVATE ${HARDENING_MACRODEFS})
endfunction(harden)
