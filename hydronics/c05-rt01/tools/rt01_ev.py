"""RT01-V: expansion-vessel duty in both directions for each C05 shared domain.

Physics (isothermal gas, absolute pressures, IAPWS-95 water density via CoolProp):
  water in EV at system pressure p:  Vw(p) = Vn (1 - p0/p)  for p > p0 else 0
  expansion to be absorbed:          dV = Vsys (rho(T1)/rho(T2) - 1)
Domain water Vsys = C05 'known geometric subtotal' + 1 L unknown allowance (C05)
(the EV's own content is NOT expanding system water; C05 adds 12 L per EV and a
1.5 factor on 4 %).
Scenarios per domain (single EV, Vn = 12 L, RV-limited max 2.8 barg as C05):
  X1 cold-filled domain heated by leak-by/residual heat to 90 C (bounding)
  C1 hot domain isolated at the minimum admitted source pressure, cooled 82 -> 10 C
     (every trip of a hot bed): needs EV water >= contraction, else p -> p_vap.
Source contract D07: 0.10..0.20 MPa(g) at z0 (C05 [S]); EV elevation vs z0 unknown,
so the check is reported against pressure at the EV.
"""
from CoolProp.CoolProp import PropsSI
from rt01_common import jload, save_csv

VN = 12.0; P_MAX = 2.8 + 1.01325


def rho(T, p_barg=1.5):
    return PropsSI("D", "T", T + 273.15, "P", (p_barg + 1.01325) * 1e5, "Water")


def vw(p_abs, p0_abs):
    return VN * (1 - p0_abs / p_abs) if p_abs > p0_abs else 0.0


def p_after(vw0, dv, p0_abs):
    """pressure (bar a) after the EV water changes by +dv from vw0."""
    v = vw0 + dv
    if v <= 0:
        return None            # vessel empty: water-only system, pressure collapses
    return p0_abs / (1 - v / VN)


if __name__ == "__main__":
    doms = [d for d in jload("internal/C05_EV_VOLUME_DOMAINS.json") if d["mode"] in ("H1", "H2")]
    dmax = max(doms, key=lambda d: d["known_geometric_water_subtotal_l"])
    vmax = dmax["known_geometric_water_subtotal_l"] + dmax["commodity_connector_unknown_allowance_l"]
    c05_req = max(27, dmax["known_geometric_water_subtotal_l"] + 13) * 0.04 * 1.5
    out = []
    for p0g in (1.0, 2.5, 0.7):
        p0 = p0g + 1.01325
        for p_op in (1.0, 1.5, 2.0):            # pressure at the EV (barg)
            pa = p_op + 1.01325
            x1 = vmax * (rho(10) / rho(90) - 1)
            c1 = vmax * (1 - rho(82) / rho(10))      # water the EV must return on cooling
            vw_fill = vw(pa, p0)
            p_x1 = p_after(vw_fill, x1, p0)
            vw_hot = vw(pa, p0)
            p_c1 = p_after(vw_hot, -c1, p0)
            out.append(dict(precharge_barg=p0g, p_at_EV_barg=p_op, V_domain_l=round(vmax, 2),
                            EV_water_at_p_l=round(vw_fill, 3),
                            X1_expansion_10_to_90C_l=round(x1, 3),
                            X1_final_barg=round(p_x1 - 1.01325, 3) if p_x1 else None,
                            X1_ok=bool(p_x1 and p_x1 <= P_MAX),
                            C1_contraction_82_to_10C_l=round(c1, 3),
                            C1_final_barg=round(p_c1 - 1.01325, 3) if p_c1 else "VACUUM",
                            C1_ok=bool(p_c1 and p_c1 > 1.2),
                            C05_required_l=round(c05_req, 3)))
            print(out[-1])
    save_csv("rt01_ev_two_direction.csv", out)
