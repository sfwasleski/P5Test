from commands2 import Command, Subsystem
from phoenix5 import TalonSRX, TalonSRXControlMode, NeutralMode, FeedbackDevice

from constants import Constants
from subsystems.coralcanon.coralcanonconstants import CoralCanonConstants


class CoralCanon(Subsystem):
    def __init__(self) -> None:
        self.left = TalonSRX(Constants.CanIds.CORAL_CANNON_LEFT_MOTOR)
        self._configure_motor(self.left)
        #self.left.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Relative)

        self.right = TalonSRX(Constants.CanIds.CORAL_CANNON_RIGHT_MOTOR)
        self._configure_motor(self.right)
        self.right.follow(self.left)
        self.right.setInverted(True)
    
    def _configure_motor(self, motor: TalonSRX):
        motor.configFactoryDefault()
        motor.setNeutralMode(NeutralMode.Brake)

    def intake_command(self) -> Command:
        return self.runEnd(lambda: self._intake(), lambda: self._stop())

    def shoot_command(self) -> Command:
        return self.runEnd(lambda: self._shoot(), lambda: self._stop())

    def _intake(self) -> None:
        self.left.set(
            TalonSRXControlMode.PercentOutput, CoralCanonConstants.INTAKE_PERCENT_OUTPUT
        )

    def _shoot(self) -> None:
        self.left.set(
            TalonSRXControlMode.PercentOutput, CoralCanonConstants.SHOOT_PERCENT_OUTPUT
        )

    def _stop(self) -> None:
        self.left.set(TalonSRXControlMode.PercentOutput, 0.0)
