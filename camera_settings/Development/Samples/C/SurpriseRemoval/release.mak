# It is assumed that the compiler has been configured so that it can
# find its standard headers and libraries without explicit -I and -L
# options. See the Borland documentation for details.
# PYLON_DEV_DIR expands to the development directory of the Pylon installation.
# Its value is taken from the environment.
!include ..\include.mak
CC			= bcc32
CPPFLAGS	= -I"$(PYLON_DEV_DIR)\Include" -DNDEBUG
CFLAGS		= -6 -OS -O2 -v-
LDFLAGS		= -L"$(PYLON_DEV_DIR)\Lib\Win32"

PROJECT     = SurpriseRemoval

bcc-release\$(PROJECT).exe:	$(PROJECT).c
	if not exist $:. md $:
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) -n$: $? $(LIBS)

clean:
	-del bcc-release\$(PROJECT).obj
	-del bcc-release\$(PROJECT).exe
