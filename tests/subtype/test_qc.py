# -*- coding: utf-8 -*-

import pandas as pd

from biohansel.subtype.qc import is_overall_coverage_low, is_maybe_intermediate_subtype, QC
from biohansel.subtype.subtype import Subtype
from biohansel.subtype.subtyper import subtype_reads, subtype_contigs
from biohansel.subtype.util import init_subtyping_params

genome_name = 'test'


def test_is_overall_coverage_low():
    st = Subtype(sample='test',
                 file_path='tests/data/subtype/Retro1000data/10-1358.fastq',
                 scheme='enteritidis',
                 are_subtypes_consistent=True,
                 avg_tile_coverage=1)
    params = init_subtyping_params(low_coverage_warning=2)
    qc_status, qc_messages = is_overall_coverage_low(st, None, params)
    assert qc_status == QC.WARNING
    assert qc_messages == "Low coverage for all tiles (1.000 < 2 expected)"


def test_low_coverage():
    scheme = 'heidelberg'
    fastq = 'tests/data/subtype/SRR1696752/SRR1696752.fastq'
    st, df = subtype_reads(reads=fastq, genome_name=genome_name, scheme=scheme)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.is_fastq_input()
    assert st.scheme == scheme
    assert 'Low coverage for all tiles (7.439 < 20 expected)' in st.qc_message
    assert st.qc_status == QC.FAIL


def test_intermediate_subtype():
    scheme = 'enteritidis'
    st = Subtype(sample='test',
                 file_path='tests/data/subtype/Retro1000data/10-1358.fastq',
                 scheme='enteritidis',
                 scheme_version='0.8.0',
                 subtype='2.1.1.2',
                 non_present_subtypes=[],
                 all_subtypes='2; 2.1; 2.1.1; 2.1.1.2',
                 inconsistent_subtypes=None,
                 tiles_matching_subtype='308238-2.1.1.2; 2469336-2.1.1.2; 3872935-2.1.1.2',
                 negative_tiles_matching_subtype=None,
                 are_subtypes_consistent=True,
                 n_tiles_matching_all=183,
                 n_tiles_matching_positive=12,
                 n_tiles_matching_negative=171,
                 n_tiles_matching_subtype=3,
                 n_tiles_matching_all_expected='188',
                 n_tiles_matching_positive_expected='15',
                 n_tiles_matching_negative_expected=0,
                 n_tiles_matching_subtype_expected='6',
                 n_negative_tiles_matching_subtype_expected=0,
                 avg_tile_coverage=37.04102564102564,
                 qc_status=None,
                 qc_message=None)
    df = pd.read_csv('tests/data/subtype/se_intermediate_subtype_df.csv')
    params = init_subtyping_params(args=None, scheme=scheme)
    st.qc_status, st.qc_message = is_maybe_intermediate_subtype(st, df, params)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.scheme == scheme
    assert "Total subtype matches observed (n=3) vs expected (n=6)" in st.qc_message
    assert st.qc_status == QC.WARNING


def test_missing_tiles():
    scheme = 'heidelberg'
    fastq = 'tests/data/subtype/SRR1696752/SRR1696752.fastq'
    st, df = subtype_reads(reads=fastq, genome_name=genome_name, scheme=scheme)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.is_fastq_input()
    assert st.scheme == scheme
    assert 'Low coverage depth (10.9 < 20.0 expected)' in st.qc_message
    assert st.qc_status == QC.FAIL


def test_mixed_tiles():
    scheme = 'heidelberg'
    fastqs = ['tests/data/subtype/SRR3392166/SRR3392166.fastq', 'tests/data/subtype/SRR3392166/SRR3392166.fastq']
    st, df = subtype_reads(reads=fastqs, genome_name=genome_name, scheme=scheme)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.scheme == scheme
    assert 'Mixed subtypes found: "1; 2; 2.1"' in st.qc_message
    assert st.qc_status == QC.FAIL


def test_mixed_subtype_positive_negative_tiles_same_target():
    scheme = 'heidelberg'
    fasta = 'tests/data/subtype/fail-qc-mixed-subtype-pos-neg-tiles.fasta'
    st, df = subtype_contigs(fasta_path=fasta, genome_name=genome_name, scheme=scheme)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.scheme == scheme
    assert st.qc_status == QC.FAIL
    expected_qc_msg = ('FAIL: Mixed subtype; the positive and negative tiles were found for the same '
                       'target sites 202001, 600783, 1049933, 1193219, 2778621, 2904061, '
                       '3278067, 3867228, 4499501, 4579224, 4738855, 202001, '
                       '600783, 1049933, 1193219, 2778621, 2904061, 3278067, '
                       '3867228, 4499501, 4579224, 4738855 for subtype "1.1".')
    assert expected_qc_msg in st.qc_message


def test_unconfident_subtype():
    scheme = 'enteritidis'
    fasta = 'tests/data/subtype/fail-qc-unconfident-subtype.fasta'
    st, df = subtype_contigs(fasta_path=fasta, genome_name=genome_name, scheme=scheme)
    assert isinstance(st, Subtype)
    assert isinstance(df, pd.DataFrame)
    assert st.scheme == scheme
    assert st.qc_status == QC.FAIL
    assert QC.UNCONFIDENT_RESULTS_ERROR_4 in st.qc_message
    assert "tiles for downstream subtype(s)" in st.qc_message
    assert "'2.1.1.1'" in st.qc_message
    assert "'2.1.1.2'" in st.qc_message
