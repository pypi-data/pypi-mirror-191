from typing import List
from pathlib import Path

import subprocess
import logging


class QiimeCommandException(Exception):
    pass


def logProcessOutput(output: bytes) -> None:
    line = output.decode("UTF-8")
    if line.strip() == "":
        return

    logging.getLogger("coretexpylib").info(line)


def QiimeCommand(args: List[str]) -> None:
    process = subprocess.Popen(
        args,
        shell = False,
        cwd = Path(__file__).parent,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # stdout, stderr = process.communicate()
    while code := process.poll() is None:
        stdout = process.stdout
        if stdout is not None:
            logProcessOutput(stdout.readline())

        stderr = process.stderr
        if stderr is not None:
            logProcessOutput(stderr.readline())

    if code != 0:
        raise QiimeCommandException


def toolsImport(sequenceType: str, inputPath: str, outputPath: str) -> None:
    QiimeCommand([
        "qiime", "tools", "import",
        "--type", sequenceType,
        "--input-path", inputPath,
        "--output-path", outputPath
    ])


def demuxEmpSingle(
    sequencesPath: str,
    barcodesPath: str,
    barcodesColumn: str,
    perSampleSequences: str,
    errorCorretctionDetailsPath: str
) -> None:

    QiimeCommand([
        "qiime", "demux", "emp-single",
        "--i-seqs", sequencesPath,
        "--m-barcodes-file", barcodesPath,
        "--m-barcodes-column", barcodesColumn,
        "--o-per-sample-sequences", perSampleSequences,
        "--o-error-correction-details", errorCorretctionDetailsPath,
        "--verbose"
    ])


def demuxSummarize(dataPath: str, visualizationPath: str) -> None:
    QiimeCommand([
        "qiime", "demux", "summarize",
        "--i-data", dataPath,
        "--o-visualization", visualizationPath
    ])


def dada2DenoiseSingle(
    inputPath: str,
    trimLeft: int,
    truncLen: int,
    representativeSequencesPath: str,
    tablePath: str,
    denoisingStatsPath: str
) -> None:

    QiimeCommand([
        "qiime", "dada2", "denoise-single",
        "--i-demultiplexed-seqs", inputPath,
        "--p-trim-left", str(trimLeft),
        "--p-trunc-len", str(truncLen),
        "--o-representative-sequences", representativeSequencesPath,
        "--o-table", tablePath,
        "--o-denoising-stats", denoisingStatsPath
    ])


def metadataTabulate(inputFile: str, visualizationPath: str) -> None:
    QiimeCommand([
        "qiime", "metadata", "tabulate",
        "--m-input-file", inputFile,
        "--o-visualization", visualizationPath
    ])


def featureTableSummarize(inputPath: str, visualizationPath: str, metadataPath: str) -> None:
    QiimeCommand([
        "qiime", "feature-table", "summarize",
        "--i-table", inputPath,
        "--o-visualization", visualizationPath,
        "--m-sample-metadata-file", metadataPath
    ])


def featureTableTabulateSeqs(inputPath: str, visualizationPath: str) -> None:
    QiimeCommand([
        "qiime", "feature-table", "tabulate-seqs",
        "--i-data", inputPath,
        "--o-visualization", visualizationPath
    ])


def phylogenyAlignToTreeMafftFasttree(
    sequencesPath: str,
    aligmentPath: str,
    maskedAligmentPath: str,
    unrootedTreePath: str,
    rootedTreePath: str
) -> None:

    QiimeCommand([
        "qiime", "phylogeny", "align-to-tree-mafft-fasttree",
        "--i-sequences", sequencesPath,
        "--o-alignment", aligmentPath,
        "--o-masked-alignment", maskedAligmentPath,
        "--o-tree", unrootedTreePath,
        "--o-rooted-tree", rootedTreePath
    ])


def diversityCoreMetricsPhylogenetic(
    phlogenyPath: str,
    tablePath: str,
    samplingDepth: int,
    metadataPath: str,
    outputDir: str
) -> None:

    QiimeCommand([
        "qiime", "diversity", "core-metrics-phylogenetic",
        "--i-phylogeny", phlogenyPath,
        "--i-table", tablePath,
        "--p-sampling-depth", str(samplingDepth),
        "--m-metadata-file", metadataPath,
        "--output-dir", outputDir
    ])


def diversityAlphaGroupSignificance(
    alphaDiversityPath: str,
    metadataPath: str,
    visualizationPath: str
) -> None:

    QiimeCommand([
        "qiime", "diversity", "alpha-group-significance",
        "--i-alpha-diversity", alphaDiversityPath,
        "--m-metadata-file", metadataPath,
        "--o-visualization", visualizationPath
    ])


def diversityBetaGroupSignificance(
    distanceMatrixPath: str,
    metadataPath: str,
    metadataColumn: str,
    visualizationPath: str,
    pairwise: bool
) -> None:

    QiimeCommand([
        "qiime", "diversity", "beta-group-significance",
        "--i-distance-matrix", distanceMatrixPath,
        "--m-metadata-file", metadataPath,
        "--m-metadata-column", metadataColumn,
        "--o-visualization", visualizationPath,
        "--p-pairwise" if pairwise else ""
    ])


def emperorPlot(
    pcoaPath: str,
    metadataPath: str,
    customAxes: str,
    visualizationPath: str
) -> None:

    QiimeCommand([
        "qiime", "emperor", "plot",
        "--i-pcoa", pcoaPath,
        "--m-metadata-file", metadataPath,
        "--p-custom-axes", customAxes,
        "--o-visualization", visualizationPath
    ])


def diversityAlphaRarefaction(
    tablePath: str,
    phylogenyPath: str,
    maxDepth: int,
    metadataPath: str,
    visualizationPath: str
) -> None:

    QiimeCommand([
        "qiime", "diversity", "alpha-rarefaction",
        "--i-table", tablePath,
        "--i-phylogeny", phylogenyPath,
        "--p-max-depth", str(maxDepth),
        "--m-metadata-file", metadataPath,
        "--o-visualization", visualizationPath
    ])


def featureClassifierClassifySklearn(
    classifierPath: str,
    readsPath: str,
    classificationPath: str
) -> None:

    QiimeCommand([
        "qiime", "feature-classifier", "classify-sklearn",
        "--i-classifier", classifierPath,
        "--i-reads", readsPath,
        "--o-classification", classificationPath
    ])


def taxaBarplot(
    tablePath: str,
    taxonomyPath: str,
    metadataPath: str,
    visualizationPath: str
) -> None:

    QiimeCommand([
        "qiime", "taxa", "barplot",
        "--i-table", tablePath,
        "--i-taxonomy", taxonomyPath,
        "--m-metadata-file", metadataPath,
        "--o-visualization", visualizationPath
    ])


def featureTableFilterSamples(
    tablePath: str,
    metadataPath: str,
    where: str,
    filteredTablePath: str
) -> None:

    QiimeCommand([
        "qiime", "feature-table", "filter-samples",
        "--i-table", tablePath,
        "--m-metadata-file", metadataPath,
        "--p-where", where,
        "--o-filtered-table", filteredTablePath
    ])


def compositionAddPseudocount(tablePath: str, compositionTablePath: str) -> None:
    QiimeCommand([
        "qiime", "composition", "add-pseudocount",
        "--i-table", tablePath,
        "--o-composition-table", compositionTablePath
    ])


def compositionAncom(
    tablePath: str,
    metadataPath: str,
    metadataColumn: str,
    visualizationPath: str
) -> None:

    QiimeCommand([
        "qiime", "composition", "ancom",
        "--i-table", tablePath,
        "--m-metadata-file", metadataPath,
        "--m-metadata-column", metadataColumn,
        "--o-visualization", visualizationPath
    ])


def taxaCollapse(
    tablePath: str,
    taxonomyPath: str,
    level: int,
    collapsedTablePath: str
) -> None:

    QiimeCommand([
        "qiime", "taxa", "collapse",
        "--i-table", tablePath,
        "--i-taxonomy", taxonomyPath,
        "--p-level", str(level),
        "--o-collapsed-table", collapsedTablePath
    ])
