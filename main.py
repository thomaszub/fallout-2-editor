#!/usr/bin/env python

import os
import sys
import cmd

from f2_save_file import F2SaveFile


class EditShell(cmd.Cmd):
    """Basic shell for F2SaveFile."""

    prompt = "Command: "
    intro = """Fallout 2 Save Game Editor. <Tab> completion is available everywhere.
The file is edited as soon as you make a change. ('exit' to exit.)"""

    def __init__(self, save_file):
        self.save_file = save_file
        self.skills = self.save_file.skills.keys()
        self.perks = self.save_file.perks.keys()
        self.save_file.print_info()
        cmd.Cmd.__init__(self)

    def do_skills(self, ignored_line):
        """skills
        List skills and current values."""
        self.save_file.print_skills()

    def do_perks(self, ignored_line):
        """perks
        List perks and current values."""
        self.save_file.print_perks()

    def do_stats(self, ignored_line):
        """stats
        List stats and current values."""
        self.save_file.print_stats()

    def __get_completion(self, text, keys):
        """Generate tab completion values."""
        if not text:
            compl = keys
        else:
            compl = [k for k in keys if k.startswith(text)]
        return compl

    def _modify_value(self, name, getter, setter):
        """Wrapper for the modifier functions."""
        try:
            value = input(f"[Value: {getter(name)}] New value: ")
        except KeyError as exc:
            print(str(exc))
            return
        try:
            value = int(value)
            if value < 0:
                raise ValueError()
        except ValueError:
            print("Positive integer required.")
            return
        setter(name, value)
        print("Done.")

    def do_set_skill(self, skill):
        """set_skill [skill]
        Modify skill values."""
        self._modify_value(skill, self.save_file.get_skill, self.save_file.set_skill)

    def complete_set_skill(self, text, line, b_ind, e_ind):
        return self.__get_completion(text, self.save_file.skills.keys())

    def do_set_perk(self, perk):
        """set_perk [perk]
        Modify perks. The correct value is 1 for most perks, but some can be stacked."""
        self._modify_value(perk, self.save_file.get_perk, self.save_file.set_perk)

    def complete_set_perk(self, text, line, b_ind, e_ind):
        return self.__get_completion(text, self.save_file.perks.keys())

    def do_set_stat(self, stat):
        """set_stat [stat]
        Modify stats. Values are limited to be in [1, 10]."""
        self._modify_value(stat, self.save_file.get_stat, self.save_file.set_stat)

    def complete_set_stat(self, text, line, b_ind, e_ind):
        return self.__get_completion(text, self.save_file.stats)

    def do_exit(self, line):
        """exit
        Terminate shell"""
        exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Exactly one argument expected: the path to the saved games.")
        exit(1)
    save_path = sys.argv[1]
    try:
        slots = os.listdir(save_path)
    except OSError as exc:
        print(f"Unable to list files in: {save_path}")
        print(exc)
        exit(1)
    print("Choose save to edit:")
    for i, slot in enumerate(slots):
        print(f"[{i}]\t{slot}")
    try:
        slot = int(input(f"<0 - {len(slots) - 1}> Edit: "))
    except ValueError:
        print("You need an integer.")
        exit(1)
    if slot > len(slots) or slot < 0:
        print("Invalid slot.")
        exit(1)
    save = F2SaveFile(os.path.join(save_path, slots[slot]))
    EditShell(save).cmdloop()
