REM loop over all directories and call make for each of them
REM aborts if any make fails and returns an error

for /D %%d in (*) do pushd %%d% & make || (popd & exit /B 1) & popd
