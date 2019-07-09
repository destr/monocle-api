isEmpty(output_dir) {
    output_dir=$$builddir/jsonproto
}
isEmpty(output_type) {
    output_type=cpp
    output_ext=hpp
}

apibgen_root_dir=$$PWD
apib_gen.name = Generate proto header
apib_gen.input = APIBFILES
apib_gen.output = $$output_dir/${QMAKE_FILE_BASE}.$$output_ext
apib_gen.commands = python3 $$apibgen_root_dir/scripts/apibgen.py -i ${QMAKE_FILE_NAME} -o ${QMAKE_FILE_OUT} \
    -m $$apibgen_root_dir/jsonproto/${QMAKE_FILE_BASE}map.txt -t $$output_type
apib_gen.variable_out = GENERATED_FILE_APIB
apib_gen.depends += $$$$apibgen_root_dir/scripts/apibgen.py $$apibgen_root_dir/scripts/jsonprotogen.py $$apibgen_root_dir/jsonproto/${QMAKE_FILE_BASE}map.txt
apib_gen.CONFIG += target_predeps
QMAKE_EXTRA_COMPILERS += apib_gen
HEADERS += $${GENERATED_FILE_APIB}
