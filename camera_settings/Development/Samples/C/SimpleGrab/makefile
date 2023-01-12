CONFIGS		= debug release

all: debug release

$(CONFIGS):
	$(MAKE) -f$@.mak

clean:
	$(MAKE) -fdebug.mak clean
	$(MAKE) -frelease.mak clean
