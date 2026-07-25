"""Run configuration. GF_ENABLED controls whether the numerical gradient-flow
corroboration runs (it is heavy: multi-core CPU).  The baseline keeps it off
(fast symbolic-only); the gf-corroboration child experiment flips it on.  This
is the only knob that varies between experiment nodes -- the run command is
identical everywhere (cardinal rule: vary code, not the command)."""

GF_ENABLED = True
