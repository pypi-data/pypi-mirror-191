from math import pi
import jax
import jax.numpy as jnp
from ..constants import EulerGamma, gt, m_per_Mpc, C
from ..typing import Array

from ripple import Mc_eta_to_ms


def get_inspiral_phase(fM_s: Array, theta: Array, coeffs: Array) -> Array:
    """
    Calculate the inspiral phase for the IMRPhenomD waveform.
    """
    # First lets calculate some of the vairables that will be used below
    # Mass variables
    m1, m2, chi1, chi2 = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    eta = m1_s * m2_s / (M_s**2.0)
    delta = jnp.sqrt(1.0 - 4.0 * eta)

    # Spin variables
    chis = chi1 + chi2
    chia = chi1 - chi2

    # These are the TaylorF2 terms used in IMRPhenomXAS
    phi0 = 1.0
    phi1 = 0.0
    phi2 = 55.0 * eta / 9.0 + 3715.0 / 756.0
    phi3 = 113.0 * delta * chia / 3.0 + (113.0 / 3.0 + 76.0 * eta / 3.0) - 16.0 * pi
    phi4 = (
        -405.0 * delta * chia * chis / 4.0
        + (200.0 * eta - 405.0 / 8.0) * chia**2.0
        + (5.0 * eta / 2.0 - 405.0 / 8.0) * chis**2.0
        + 15293365.0 / 508032.0
        + 27145.0 * eta / 504.0
        + 3085.0 * eta**2.0 / 72.0
    )
    phi5 = (
        chia
        * (
            -140.0 * delta * eta / 9.0
            - 732985.0 * delta / 2268.0
            + (-140.0 * delta * eta / 9.0 - 732985.0 * delta / 2268.0)
            * jnp.log(pi * fM_s)
        )
        + chis
        * (
            (340.0 * eta**2.0 / 9.0 + 24260.0 * eta / 81.0 - 732985.0 / 2268.0)
            * jnp.log(pi * fM_s)
            + 340.0 * eta**2.0 / 9.0
            + 24260.0 * eta / 81.0
            - 732985.0 / 2268.0
        )
        + (38645.0 * pi / 756.0 - 65.0 * pi * eta / 9.0) * jnp.log(pi * fM_s)
        - 65.0 * pi * eta / 9.0
        + 38645.0 * pi / 756.0
    )
    phi6 = (
        chis
        * (
            chia * (75515.0 * delta / 144.0 - 8225.0 * delta * eta / 18.0)
            - 520.0 * pi * eta
            + 2270.0 * pi / 3.0
        )
        + 2270.0 * pi * delta * chia / 3.0
        - 6848.0 * jnp.log(pi * fM_s) / 63.0
        - 127825.0 * eta**3 / 1296.0
        + (-480.0 * eta**2.0 - 263245.0 * eta / 252.0 + 75515.0 / 288.0) * chia**2.0
        + (1255.0 * eta**2.0 / 9.0 - 232415.0 * eta / 504.0 + 75515.0 / 288.0)
        * chis**2.0
        + 76055.0 * eta**2 / 1728.0
        + 2255.0 * pi**2.0 * eta / 12.0
        - 15737765635.0 * eta / 3048192.0
        - 640.0 * pi**2.0 / 3.0
        - 6848.0 * EulerGamma / 21.0
        + 11583231236531.0 / 469415680.0
        - 13696.0 * jnp.log(2) / 21.0
    )
    phi7 = (
        chia
        * (
            -1985.0 * delta * eta**2.0 / 48.0
            + 26804935.0 * delta * eta / 6048.0
            - 25150083775.0 * delta / 3048192.0
        )
        + chis
        * (
            -1140 * pi * delta * chia
            + 5345.0 * eta**3.0 / 36.0
            + (80.0 * eta**2.0 - 7270.0 * eta + 14585.0 / 8.0) * chia**2.0
            - 1042165.0 * eta**2.0 / 3024.0
            + 10566655595.0 * eta / 762048.0
            - 25150083775.0 / 3048192.0
        )
        + chia**3.0 * (14585.0 * delta / 24.0 - 2380.0 * delta * eta)
        + chis**2.0
        * (
            chia * (14585.0 * delta / 8.0 - 215.0 * delta * eta / 2.0)
            + 40.0 * pi * eta
            - 570.0 * pi
        )
        + chis**3.0 * (100 * eta**2.0 / 3.0 - 475 * eta / 6.0 + 14585.0 / 24.0)
        - 74045.0 * pi * eta**2.0 / 756.0
        + (2240.0 * pi * eta - 570.0 * pi) * chia**2
        + 378515.0 * pi * eta / 1512.0
        + 77096675.0 * pi / 254016.0
    )
    phi8 = pi * (
        chia
        * (
            -99185.0 * delta * eta / 252.0
            + 233915.0 * delta / 168.0
            + (99185.0 * delta * eta / 252.0 - 233915.0 * delta / 168.0)
            * jnp.log(pi * fM_s)
        )
        + chis
        * (
            (-19655.0 * eta**2 / 189.0 + 3970375.0 * eta / 2268.0 - 233915.0 / 168.0)
            * jnp.log(pi * fM_s)
            + 19655.0 * eta**2 / 189.0
            - 3970375.0 * eta / 2268.0
            + 233915.0 / 168.0
        )
    )

    phi_TF2 = -pi / 4.0 + (
        phi0 * ((pi * fM_s) ** -(5.0 / 3.0))
        + phi1 * ((pi * fM_s) ** -(4.0 / 3.0))
        + phi2 * ((pi * fM_s) ** -1.0)
        + phi3 * ((pi * fM_s) ** -(2.0 / 3.0))
        + phi4 * ((pi * fM_s) ** -(1.0 / 3.0))
        + phi5
        + phi6 * ((pi * fM_s) ** (1.0 / 3.0))
        + phi7 * ((pi * fM_s) ** (2.0 / 3.0))
        + phi8 * ((pi * fM_s))
    ) * (3.0 / (128.0 * eta))

    sigma1 = 1.0
    sigma2 = 1.0
    sigma3 = 1.0
    sigma4 = 1.0
    sigma5 = 1.0

    phi_Ins = (
        phi_TF2
        + (
            sigma1 * fM_s
            + (3.0 / 4.0) * sigma2 * (fM_s ** (4.0 / 3.0))
            + (3.0 / 5.0) * sigma3 * (fM_s ** (5.0 / 3.0))
            + (1.0 / 2.0) * sigma4 * (fM_s**2.0)
            + (3.0 / 7.0) * sigma5 * (fM_s ** (7.0 / 3.0))
        )
        / eta
    )

    return phi_Ins


def get_intermediate_raw_phase(fM_s: Array, theta: Array, coeffs: Array) -> Array:
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    eta = m1_s * m2_s / (M_s**2.0)

    return None


def get_mergerringdown_raw_phase(
    fM_s: Array, theta: Array, coeffs: Array, f_RD, f_damp
) -> Array:
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    eta = m1_s * m2_s / (M_s**2.0)

    return None


def get_Amp0(fM_s: Array, eta: float) -> Array:
    Amp0 = (
        (2.0 / 3.0 * eta) ** (1.0 / 2.0) * (fM_s) ** (-7.0 / 6.0) * pi ** (-1.0 / 6.0)
    )
    return Amp0


def get_inspiral_Amp(fM_s: Array, theta: Array) -> Array:
    m1, m2, chi1, chi2 = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    eta = m1_s * m2_s / (M_s**2.0)
    eta2 = eta * eta
    eta3 = eta * eta2
    delta = jnp.sqrt(1.0 - 4.0 * eta)

    # Spin variables
    chi12 = chi1 * chi1
    chi22 = chi2 * chi2

    chi13 = chi12 * chi1
    chi23 = chi22 * chi2

    A0 = 1.0
    A2 = -323.0 / 224.0 + 451.0 * eta / 168.0
    A3 = chi1 * (27.0 * delta / 16.0 - 11.0 * eta / 12.0 + 27.0 / 16.0) + chi2 * (
        -27.0 * delta / 16.0 - 11.0 * eta / 12.0 + 27.0 / 16.0
    )
    A4 = (
        chi12 * (-81.0 * delta / 64.0 + 81.0 * eta / 32.0 - 81.0 / 64.0)
        + chi22 * (81.0 * delta / 64.0 + 81.0 * eta / 32.0 - 81.0 / 64.0)
        + (
            105271.0 * eta2 / 24192.0
            - 1975055.0 * eta / 338688
            - 27312085.0 / 8128512.0
        )
        - 47.0 * eta * chi1 * chi2 / 16.0
    )
    A5 = (
        chi13 * (delta * (3.0 / 16.0 - 3 * eta / 16.0) - 9.0 * eta / 16.0 + 3.0 / 16.0)
        + chi1
        * (
            delta * (287213.0 / 32256.0 - 2083.0 * eta / 8064.0)
            - 2227.0 * eta2 / 2016.0
            - 15569.0 * eta / 1344.0
            + 287213.0 / 32256.0
        )
        + chi23
        * (delta * (3.0 * eta / 16.0 - 3.0 / 16.0) - 9.0 * eta / 16.0 + 3.0 / 16.0)
    )
    (
        +chi2
        * (
            delta * (2083.0 * eta / 8064.0 - 287213.0 / 32256.0)
            - 2227.0 * eta2 / 2016.0
            - 15569.0 * eta / 1344.0
            + 287213.0 / 32256.0
        )
        - 85.0 * pi / 64.0
        + 85.0 * pi * eta / 16.0
    )
    A6 = (
        (
            chi1
            * (
                -17.0 * pi * delta / 12.0
                + (-133249.0 * eta2 / 8064.0 - 319321.0 * eta / 32256.0) * chi2
                + 5.0 * pi * eta / 3.0
                - 17.0 * pi / 12.0
            )
            + chi12
            * (
                delta * (-141359.0 * eta / 32256.0 - 49039.0 / 14336.0)
                + 163199.0 * eta2 / 16128.0
                + 158633.0 * eta / 64512.0
                - 49039.0 / 14336.0
            )
            + chi22
            * (
                delta * (141359.0 * eta / 32256.0 - 49039.0 / 14336.0)
                + 163199.0 * eta2 / 16128.0
                + 158633.0 * eta / 64512.0
                - 49039.0 / 14336.0
            )
        )
        + chi2 * (17.0 * pi * delta / 12.0 + 5 * pi * eta / 3.0 - 17 * pi / 12.0)
        - 177520268561.0 / 8583708672.0
        + (545384828789.0 / 5007163392.0 - 205.0 * pi**2.0 / 48.0) * eta
        - 3248849057.0 * eta2 / 178827264.0
        + 34473079.0 * eta3 / 6386688.0
    )

    # Here we need to compute the rhos
    # A7 = rho1
    # A8 = rho2
    # A9 = rho3

    Amp_Ins = (
        A0
        # A1 is missed since its zero
        + A2 * (fM_s ** (2.0 / 3.0))
        + A3 * fM_s
        + A4 * (fM_s ** (4.0 / 3.0))
        + A5 * (fM_s ** (5.0 / 3.0))
        + A6 * (fM_s**2.0)
        # # Now we add the coefficient terms
        # + A7 * (fM_s ** (7.0 / 3.0))
        # + A8 * (fM_s ** (8.0 / 3.0))
        # + A9 * (fM_s ** 3.0)
    )

    return Amp_Ins


def get_intermediate_Amp(
    fM_s: Array, theta: Array, coeffs: Array, f1, f3, f_RD, f_damp
) -> Array:
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s

    return None


def get_mergerringdown_Amp(
    fM_s: Array, theta: Array, coeffs: Array, f_RD, f_damp
) -> Array:
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    return None


@jax.jit
def Phase(f: Array, theta: Array) -> Array:
    """
    Computes the phase of the PhenomD waveform following 1508.07253.
    Sets time and phase of coealence to be zero.

    Returns:
    --------
        phase (array): Phase of the GW as a function of frequency
    """
    # First lets calculate some of the vairables that will be used below
    # Mass variables
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s

    # And now we can combine them by multiplying by a set of heaviside functions
    # phase = (
    #     phi_Ins * jnp.heaviside(f1 - f, 0.5)
    #     + jnp.heaviside(f - f1, 0.5) * phi_Inter * jnp.heaviside(f2 - f, 0.5)
    #     + phi_MR * jnp.heaviside(f - f2, 0.5)
    # )

    return None


@jax.jit
def Amp(f: Array, theta: Array, D=1) -> Array:
    """
    Computes the amplitude of the PhenomD frequency domain waveform following 1508.07253.
    Note that this waveform also assumes that object one is the more massive.

    Returns:
    --------
      Amplitude (array):
    """

    # First lets calculate some of the vairables that will be used below
    # Mass variables
    m1, m2, _, _ = theta
    m1_s = m1 * gt
    m2_s = m2 * gt
    M_s = m1_s + m2_s
    eta = m1_s * m2_s / (M_s**2.0)

    # And now we can combine them by multiplying by a set of heaviside functions
    # Amp = (
    #     Amp_Ins * jnp.heaviside(f3 - f, 0.5)
    #     + jnp.heaviside(f - f3, 0.5) * Amp_Inter * jnp.heaviside(f4 - f, 0.5)
    #     + Amp_MR * jnp.heaviside(f - f4, 0.5)
    # )

    # Prefactor
    Amp0 = get_Amp0(f * M_s, eta) * (
        2.0 * jnp.sqrt(5.0 / (64.0 * pi))
    )  # This second factor is from lalsuite...

    # Need to add in an overall scaling of M_s^2 to make the units correct
    dist_s = (D * m_per_Mpc) / C
    # return Amp0 * Amp * (M_s ** 2.0) / dist_s
    return None


@jax.jit
def _gen_IMRPhenomXAS(
    f: Array, theta_intrinsic: Array, theta_extrinsic: Array, coeffs: Array
):
    M_s = (theta_intrinsic[0] + theta_intrinsic[1]) * gt
    # Lets call the amplitude and phase now
    Psi = Phase(f, theta_intrinsic)
    A = Amp(f, theta_intrinsic, D=theta_extrinsic[0])
    h0 = A * jnp.exp(1j * -Psi)
    return h0


@jax.jit
def gen_IMRPhenomXAS(f: Array, params: Array):
    """
    Generate PhenomXAS frequency domain waveform following 2001.11412.
    Note that this waveform also assumes that object one is the more massive.
    vars array contains both intrinsic and extrinsic variables
    theta = [Mchirp, eta, chi1, chi2, D, tc, phic]
    Mchirp: Chirp mass of the system [solar masses]
    eta: Symmetric mass ratio [between 0.0 and 0.25]
    chi1: Dimensionless aligned spin of the primary object [between -1 and 1]
    chi2: Dimensionless aligned spin of the secondary object [between -1 and 1]
    D: Luminosity distance to source [Mpc]
    tc: Time of coalesence. This only appears as an overall linear in f contribution to the phase
    phic: Phase of coalesence

    Returns:
    --------
      hp (array): Strain of the plus polarization
      hc (array): Strain of the cross polarization
    """
    # Lets make this easier by starting in Mchirp and eta space
    m1, m2 = Mc_eta_to_ms(jnp.array([params[0], params[1]]))
    theta_intrinsic = jnp.array([m1, m2, params[2], params[3]])
    theta_extrinsic = jnp.array([params[4], params[5], params[6]])

    # h0 = _gen_IMRPhenomXAS(f, theta_intrinsic, theta_extrinsic, coeffs)
    return None
