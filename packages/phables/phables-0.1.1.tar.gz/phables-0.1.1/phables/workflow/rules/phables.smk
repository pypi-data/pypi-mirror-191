rule run_phables:
    input:
        GRAPH_FILE,
        COVERAGE_FILE,
        PHROG_ANNOT,
        SMG_FILE,
        preprocessTargets
    output:
        genomes_fasta = os.path.join(OUTDIR, "resolved_paths.fasta"),
        genomes_folder = directory(os.path.join(OUTDIR, "resolved_phages")),
        genome_info = os.path.join(OUTDIR, "resolved_genome_info.txt"),
        unitigs = os.path.join(OUTDIR, "resolved_edges.fasta"),
        component_info = os.path.join(OUTDIR, "resolved_component_info.txt")
    params:
        graph = GRAPH_FILE,
        hmmout = SMG_FILE,
        phrogs = PHROG_ANNOT,
        coverage = COVERAGE_FILE,
        bampath = BAM_PATH,
        minlength = ML,
        mincov = MC,
        compcount = CC,
        maxpaths = MP,
        mgfrac = MGF,
        alignscore = AS,
        seqidentity = SI,
        output = OUTDIR,
        log = os.path.join(LOGSDIR, "phables_output.log")
    log:
        os.path.join(LOGSDIR, "phables_output.log")
    conda:
        os.path.join("..", "envs", "phables.yaml")
    script:
        os.path.join("..", "scripts", "phables.py")
