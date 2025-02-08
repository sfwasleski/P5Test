from commands2 import Command, Subsystem
from phoenix5 import NeutralMode, TalonSRX, TalonSRXControlMode

from constants import Constants
from subsystems.coralcanon.coralcanonconstants import CoralCanonConstants


class CoralCanon(Subsystem):
    def __init__(self) -> None:
        self.left = TalonSRX(Constants.CanIds.CORAL_CANNON_LEFT_MOTOR)
        self._configure_motor(self.left)

        self.right = TalonSRX(Constants.CanIds.CORAL_CANNON_RIGHT_MOTOR)
        self._configure_motor(self.right)
        self.right.setInverted(True)

    def _configure_motor(self, motor: TalonSRX):
        motor.configFactoryDefault()
        motor.setNeutralMode(NeutralMode.Brake)

    def intake_command(self) -> Command:
        return self.runEnd(
            lambda: self._runStraight(CoralCanonConstants.INTAKE_PERCENT_OUTPUT),
            lambda: self._stop(),
        )

    def shoot_command(self) -> Command:
        return self.runEnd(
            lambda: self._runStraight(CoralCanonConstants.SHOOT_PERCENT_OUTPUT),
            lambda: self._stop(),
        )
    
    def shoot_L1_command(self) -> Command:
        return self.runEnd(
            lambda: self._runSpec(0.7, 0.4),
            lambda: self._stop(),
        )

    def backup_command(self) -> Command:
        return self.runEnd(
            lambda: self._runStraight(CoralCanonConstants.BACKUP_PERCENT_OUTPUT),
            lambda: self._stop(),
        )

    def _runStraight(self, leftPercentOutput) -> None:
        self._runSpec(leftPercentOutput, leftPercentOutput * 1.05)

    def _runSpec(self, leftPercentOutput, rightPercentOutput) -> None:
        self.left.set(TalonSRXControlMode.PercentOutput, leftPercentOutput)
        self.right.set(TalonSRXControlMode.PercentOutput, rightPercentOutput)

    def _stop(self) -> None:
        self.left.set(TalonSRXControlMode.PercentOutput, 0.0)
        self.right.set(TalonSRXControlMode.PercentOutput, 0.0)
