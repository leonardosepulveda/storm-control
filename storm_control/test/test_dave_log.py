"""
Test Dave's <log> tag and the creation of <change_directory> folders.
"""
import os

from PyQt5 import QtWidgets

import storm_control.dave.daveActions as daveActions
import storm_control.dave.sequenceViewer as sequenceViewer
import storm_control.dave.xml_generators.v2Generator as v2Generator

app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def makeSequence(tmp_path):
    """
    Generate a sequence from a recipe with a <log> before any
    <change_directory>, and logs around a fluidics loop and an imaging step.
    """
    hyb_dir = str(tmp_path / "data" / "H01")
    recipe = tmp_path / "recipe.xml"
    recipe.write_text("""<?xml version="1.0" encoding="ISO-8859-1"?>
<recipe>
  <command_sequence>
    <log>experiment start</log>
    <change_directory>""" + hyb_dir + """</change_directory>
    <loop name="Hyb 01 Fluidics">
      <variable_entry name="Hyb 01 Fluidics"/>
    </loop>
    <log>Hyb 01 Imaging start</log>
    <valve_protocol>Image</valve_protocol>
    <log>Hyb 01 Imaging end</log>
  </command_sequence>
  <loop_variable name="Hyb 01 Fluidics">
    <value>
      <log>Hyb 01 Fluidics start</log>
      <valve_protocol>Hybridize</valve_protocol>
      <log>Hyb 01 Fluidics end</log>
    </value>
  </loop_variable>
</recipe>
""")
    sequence = str(tmp_path / "sequence.xml")
    parser = v2Generator.XMLRecipeParser(xml_filename = str(recipe),
                                         output_filename = sequence,
                                         verbose = False)
    parser.parseXML()
    return sequence, hyb_dir


def logActions(model):
    actions = [item.getDaveAction() for item in model.dave_actions_all]
    return [a for a in actions if isinstance(a, daveActions.DALog)]


def test_log_generator(tmp_path):
    """
    Each <log> becomes a DALog in the directory of the last
    <change_directory>, or the recipe's directory before the first one.
    """
    sequence, hyb_dir = makeSequence(tmp_path)
    logs = logActions(sequenceViewer.parseSequenceFile(sequence))

    assert [(a.text, a.directory) for a in logs] == [
        ("experiment start", str(tmp_path)),
        ("Hyb 01 Fluidics start", hyb_dir),
        ("Hyb 01 Fluidics end", hyb_dir),
        ("Hyb 01 Imaging start", hyb_dir),
        ("Hyb 01 Imaging end", hyb_dir)]


def test_change_directory_creates_folder(tmp_path):
    """
    Loading a sequence creates the folders of its <change_directory> tags.
    """
    sequence, hyb_dir = makeSequence(tmp_path)
    assert not os.path.exists(hyb_dir)
    sequenceViewer.parseSequenceFile(sequence)
    assert os.path.isdir(hyb_dir)


def test_log_writes_one_file_per_event(tmp_path):
    """
    Running a DALog writes one small file; test mode (validation) writes none.
    """
    sequence, hyb_dir = makeSequence(tmp_path)
    log = logActions(sequenceViewer.parseSequenceFile(sequence))[1]
    completed = []
    log.complete_signal.connect(completed.append)

    log.start(False, True)
    assert os.listdir(hyb_dir) == []

    log.start(False, False)
    [filename] = os.listdir(hyb_dir)
    assert filename.startswith("dave_log_")
    assert filename.endswith("_Hyb_01_Fluidics_start.txt")
    with open(os.path.join(hyb_dir, filename)) as fp:
        assert fp.read().rstrip("\n").split("\t")[1] == "Hyb 01 Fluidics start"
    assert len(completed) == 2


def test_log_write_failure_is_a_warning(tmp_path):
    """
    If the file cannot be written, the action completes with a warning.
    """
    sequence, hyb_dir = makeSequence(tmp_path)
    log = logActions(sequenceViewer.parseSequenceFile(sequence))[1]
    log.directory = str(tmp_path / "a_file")
    (tmp_path / "a_file").write_text("")
    warnings = []
    log.warning_signal.connect(warnings.append)

    log.start(False, False)
    assert len(warnings) == 1
    assert "Could not write log" in warnings[0].getErrorMessage()


def test_log_runs_in_command_engine(tmp_path):
    """
    Dave's command engine runs a DALog to completion, as in a real run.
    """
    import storm_control.dave.dave as dave

    sequence, hyb_dir = makeSequence(tmp_path)
    log = logActions(sequenceViewer.parseSequenceFile(sequence))[1]
    engine = dave.CommandEngine()
    done = []
    engine.done.connect(lambda: done.append(True))

    engine.startCommand(log, test_mode = False)
    assert done == [True]
    assert len(os.listdir(hyb_dir)) == 1
