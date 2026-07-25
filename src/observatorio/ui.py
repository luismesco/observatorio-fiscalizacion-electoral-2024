from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


def ensure_src_path() -> None:
    root = Path(__file__).resolve().parents[2]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def page_setup(title: str) -> None:
    st.set_page_config(page_title=title, layout="wide")
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
        :root {
          --ink:#211816; --muted:#665a52; --line:#d7c7b2; --paper:#fff9ef; --newsprint:#f3eadc;
          --guinda:#6B1531; --guinda-dark:#3b0718; --guinda-soft:#8f2347;
          --dorado:#C59A3D; --dorado-soft:#ead7a6; --verde:#1E5B4F; --pan:#2B5C8A; --mc:#FF6600; --black:#14100d;
          --pale:#fbf2e5; --steel:#31363b; --white:#fffdf8;
        }
        html { scroll-behavior: smooth; }
        .stApp {
          background: #ffffff;
          color: var(--ink);
          font-family: "Montserrat", sans-serif !important;
        }
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"], [data-testid="stWidgetLabel"], button, input, textarea, select {
          font-family: "Montserrat", sans-serif !important;
        }
        .block-container { max-width: 1180px; padding-top: 2rem; padding-left: clamp(1rem, 3vw, 2.2rem); padding-right: clamp(1rem, 3vw, 2.2rem); padding-bottom: 6.5rem; }
        .block-container:before {
          content: "";
          display: block;
          height: 6px;
          background: linear-gradient(90deg, var(--guinda) 0 38%, var(--dorado) 38% 46%, var(--black) 46% 100%);
          margin-bottom: 18px;
        }
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }
        [data-testid="stToolbar"], .stDeployButton { display: none !important; }
        .site-nav {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 18px;
          border-bottom: 1px solid rgba(20,16,13,.24);
          padding: 12px 0 16px;
          margin: 0 0 26px;
        }
        .site-brand {
          color: var(--guinda-dark);
          font-weight: 900;
          font-size: .86rem;
          text-transform: uppercase;
          letter-spacing: 0;
        }
        .site-links {
          display: flex;
          gap: 18px;
          flex-wrap: wrap;
          justify-content: flex-end;
        }
        .site-links a {
          color: var(--muted);
          text-decoration: none;
          font-size: .72rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .site-links a.active,
        .site-links a:hover { color: var(--guinda); }
        div[data-testid="stDownloadButton"] { margin: 28px 0 24px; }
        div[data-testid="stDownloadButton"] button {
          background: var(--guinda);
          color: #fffdf8;
          border: 1px solid var(--guinda-dark);
          border-radius: 999px;
          min-height: 44px;
          padding: 0 22px;
          font-size: .74rem;
          font-weight: 900;
          text-transform: uppercase;
          box-shadow: inset 0 -3px 0 rgba(20,16,13,.18), 0 8px 18px rgba(107,21,49,.14);
        }
        div[data-testid="stDownloadButton"] button:hover {
          background: var(--guinda-dark);
          color: #fffdf8;
          border-color: var(--guinda-dark);
          transform: translateY(-1px);
        }
        div[data-testid="stDownloadButton"] button:focus:not(:active) {
          border-color: var(--dorado);
          color: #fffdf8;
          box-shadow: 0 0 0 3px rgba(197,154,61,.22), inset 0 -4px 0 rgba(20,16,13,.16);
        }
        .download-note {
          color: var(--muted);
          font-size: .82rem;
          font-weight: 750;
          line-height: 1.35;
          margin: -6px 0 16px;
        }
        .download-dock {
          position: fixed;
          right: clamp(14px, 2.6vw, 34px);
          bottom: clamp(14px, 2.4vw, 28px);
          z-index: 999;
          display: flex;
          align-items: center;
          gap: 8px;
          background: rgba(255,253,248,.94);
          border: 1px solid rgba(20,16,13,.18);
          border-top: 4px solid var(--guinda);
          padding: 10px;
          box-shadow: 0 18px 44px rgba(40,22,12,.18);
          backdrop-filter: blur(12px);
          animation: dockFloat .7s ease both .35s;
        }
        .download-dock span {
          color: var(--muted);
          font-size: .68rem;
          font-weight: 900;
          line-height: 1.05;
          text-transform: uppercase;
          max-width: 104px;
        }
        .download-dock .pill {
          border-radius: 999px;
          color: #fffdf8;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-height: 40px;
          padding: 0 16px;
          text-decoration: none;
          font-size: .72rem;
          font-weight: 900;
          text-transform: uppercase;
          box-shadow: inset 0 -3px 0 rgba(20,16,13,.18);
          transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
          white-space: nowrap;
        }
        .download-dock .pill:hover {
          transform: translateY(-2px);
          box-shadow: inset 0 -3px 0 rgba(20,16,13,.2), 0 10px 18px rgba(107,21,49,.16);
        }
        .download-dock .primary { background: var(--guinda); }
        .download-dock .secondary { background: var(--verde); }
        h1, h2, h3 { color: var(--ink); letter-spacing: 0; font-family: "Montserrat", sans-serif; overflow-wrap: normal; word-break: normal; hyphens: none; }
        h1, h2, h3,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
          font-weight: 900 !important;
          text-transform: uppercase;
        }
        h1 { font-size: clamp(2.2rem, 4vw, 4.6rem); font-weight: 900; line-height: .92; border-bottom: 4px solid var(--guinda); padding-bottom: .55rem; text-transform: uppercase; }
        h2 { font-size: 1.42rem; font-weight: 900; border-top: 6px solid var(--black); padding-top: .55rem; text-transform: uppercase; }
        h3 { font-size: 1rem; font-weight: 900; text-transform: uppercase; }
        p, li, div, span, label { letter-spacing: 0; font-family: "Montserrat", sans-serif; }
        [data-testid="stMetric"] {
          background: linear-gradient(180deg, #fffdf8, #f5eadb);
          border: 1px solid var(--line);
          border-top: 5px solid var(--guinda);
          border-radius: 0;
          padding: 16px 16px;
          box-shadow: 0 10px 24px rgba(70,45,25,.08);
          min-width: 0;
          overflow: visible;
        }
        [data-testid="stMetricLabel"] p {
          font-size: .66rem;
          font-weight: 800;
          text-transform: uppercase;
          color: var(--muted);
          white-space: normal;
          overflow-wrap: anywhere;
          line-height: 1.12;
        }
        [data-testid="stMetricValue"] {
          color: var(--guinda-dark);
          font-weight: 900;
          min-width: 0;
          overflow: visible;
        }
        [data-testid="stMetricValue"] div {
          font-size: clamp(1.45rem, 2vw, 2.2rem) !important;
          line-height: 1 !important;
          white-space: normal;
          overflow: visible !important;
          text-overflow: clip;
          overflow-wrap: normal;
          word-break: keep-all;
          hyphens: none;
        }
        .responsive-kpi-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr));
          gap: clamp(12px, 2vw, 22px);
          margin: 24px 0 38px;
        }
        .responsive-kpi {
          min-width: 0;
          background: linear-gradient(180deg, #fffdf8, #f5eadb);
          border: 1px solid var(--line);
          border-top: 5px solid var(--guinda);
          min-height: 150px;
          padding: clamp(16px, 2.1vw, 24px);
          box-shadow: 0 10px 24px rgba(70,45,25,.08);
          container-type: inline-size;
          animation: editorialRise .5s ease both;
          transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
        }
        .responsive-kpi:hover {
          transform: translateY(-3px);
          border-top-color: var(--dorado);
          box-shadow: 0 16px 34px rgba(70,45,25,.12);
        }
        .responsive-kpi .kpi-label {
          color: var(--muted);
          font-size: clamp(.64rem, 1.4vw, .72rem);
          font-weight: 900;
          line-height: 1.12;
          text-transform: uppercase;
          overflow-wrap: anywhere;
          min-height: 1.5em;
        }
        .responsive-kpi .kpi-value {
          color: var(--guinda-dark);
          display: block;
          font-size: clamp(2.05rem, 3.7vw, 3.15rem);
          font-weight: 900;
          line-height: .92;
          margin-top: 16px;
          white-space: normal;
          overflow: visible;
          overflow-wrap: normal;
          word-break: keep-all;
          hyphens: none;
        }
        .responsive-kpi .kpi-value.money {
          font-size: clamp(2.05rem, 3.5vw, 3rem);
          line-height: .9;
          overflow-wrap: normal;
          word-break: keep-all;
        }
        .responsive-kpi .kpi-detail {
          color: var(--muted);
          display: block;
          font-size: clamp(.68rem, 1vw, .82rem);
          font-weight: 850;
          line-height: 1.16;
          margin-top: 12px;
          overflow-wrap: anywhere;
          text-transform: uppercase;
        }
        @container (max-width: 170px) {
          .responsive-kpi .kpi-value { font-size: 1.75rem; }
          .responsive-kpi .kpi-value.money { font-size: 1.32rem; }
        }
        .notice { background: var(--paper); border-left: 8px solid var(--guinda); padding: 14px 16px; margin: 8px 0 18px; box-shadow: inset 0 1px 0 var(--dorado-soft); }
        .small-muted { color: var(--muted); font-size: 0.92rem; }
        div[data-testid="stSidebar"] { background: linear-gradient(180deg, #efe3d0, #e3d4be); }
        div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { font-weight: 600; }
        .print-title { border-top: 8px solid var(--guinda); border-bottom: 2px solid var(--dorado); padding: 14px 0 10px; margin-bottom: 14px; }
        .print-kicker { color: var(--verde); font-weight: 700; text-transform: uppercase; font-size: .78rem; letter-spacing: 0; }
        .source-note { color: var(--muted); font-size: .82rem; }
        .newspaper-shell {
          position: relative;
          overflow: hidden;
          background: #ffffff;
          border: 0;
          border-top: 1px solid rgba(20,16,13,.28);
          border-bottom: 1px solid rgba(20,16,13,.28);
          border-radius: 0;
          padding: 24px 0;
          box-shadow: none;
        }
        .newspaper-shell:after { display: none; }
        .masthead { position: relative; border-top: 12px solid var(--guinda); border-bottom: 4px solid var(--black); padding: 14px 0 18px; margin-bottom: 16px; z-index: 1; }
        .masthead .kicker { color: var(--guinda); font-weight: 900; text-transform: uppercase; font-size: .78rem; }
        .masthead .headline { font-family: "Montserrat", sans-serif; font-weight: 900; letter-spacing: 0; font-size: clamp(2.55rem, 5vw, 5.8rem); line-height: .86; color: var(--black); margin: .25rem 0; text-transform: uppercase; max-width: 980px; }
        .masthead .deck { max-width: 900px; color: var(--muted); font-size: 1.02rem; line-height: 1.5; font-weight: 500; }
        .editorial-grid { display: grid; grid-template-columns: 1.18fr .82fr; gap: 22px; align-items: start; }
        .folio-row { display: flex; gap: 0; flex-wrap: wrap; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 11px 0; margin: 10px 0 18px; font-size: .76rem; font-weight: 900; text-transform: uppercase; color: var(--muted); }
        .folio-row span { position: relative; background: transparent; border: 0; padding: 0 18px 0 0; margin-right: 18px; }
        .folio-row span:after { content: ""; position: absolute; right: 0; top: 50%; width: 4px; height: 4px; background: var(--dorado); transform: translateY(-50%) rotate(45deg); }
        .folio-row span:last-child:after { display: none; }
        .intro-lede {
          display: grid;
          grid-template-columns: .92fr 1.08fr;
          gap: 34px;
          align-items: end;
          margin: 22px 0 30px;
          padding-bottom: 24px;
          border-bottom: 1px solid rgba(20,16,13,.28);
        }
        .intro-kicker { color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; }
        .intro-title {
          color: var(--black);
          font-size: clamp(2.35rem, 4.5vw, 5.55rem);
          font-weight: 900;
          line-height: .98;
          text-transform: uppercase;
          margin-top: 8px;
          max-width: 720px;
        }
        .intro-title span { display: block; }
        .intro-copy {
          color: var(--muted);
          font-size: clamp(1rem, 1.45vw, 1.35rem);
          font-weight: 600;
          line-height: 1.45;
          max-width: 660px;
        }
        .sanction-board {
          display: grid;
          grid-template-columns: .8fr 1.2fr;
          gap: 34px;
          margin: 18px 0 30px;
          padding: 20px 0 26px;
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
        }
        .sanction-total { border-left: 8px solid var(--guinda); padding-left: 18px; }
        .sanction-total .label { color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; }
        .sanction-total .amount { color: var(--guinda-dark); font-size: clamp(2.6rem, 5vw, 5.5rem); font-weight: 900; line-height: .86; margin: 12px 0; }
        .sanction-total .note { color: var(--muted); font-weight: 700; line-height: 1.35; }
        .cause-list { display: grid; gap: 12px; }
        .cause-row {
          display: grid;
          grid-template-columns: minmax(180px, 1fr) minmax(140px, .72fr);
          gap: 18px;
          align-items: end;
          padding-bottom: 12px;
          border-bottom: 1px solid rgba(20,16,13,.18);
        }
        .cause-row .cause { color: var(--black); font-size: .9rem; font-weight: 900; text-transform: uppercase; }
        .cause-row .money { color: var(--guinda-dark); font-size: 1.25rem; font-weight: 900; text-align: right; }
        .plain-steps {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 24px;
          margin: 20px 0 28px;
        }
        .plain-step { border-top: 4px solid var(--dorado); padding-top: 10px; }
        .plain-step strong { display: block; color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; margin-bottom: 6px; }
        .plain-step span { color: var(--muted); font-weight: 650; line-height: 1.4; }
        .home-nav {
          position: sticky;
          top: 0;
          z-index: 5;
          background: rgba(255,255,255,.94);
          backdrop-filter: blur(10px);
        }
        .home-hero {
          display: grid;
          grid-template-columns: 1.18fr .82fr;
          gap: clamp(24px, 4vw, 58px);
          align-items: center;
          min-height: min(62vh, 560px);
          padding: clamp(32px, 5vw, 64px) 0 34px;
          border-bottom: 1px solid rgba(20,16,13,.28);
          animation: editorialRise .46s ease both;
        }
        .home-kicker {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
          margin-bottom: 12px;
        }
        .home-title {
          color: var(--black);
          font-size: clamp(3rem, 4.8vw, 4.8rem);
          font-weight: 900;
          line-height: .86;
          text-transform: uppercase;
          max-width: 820px;
          overflow-wrap: normal;
          word-break: normal;
          hyphens: none;
        }
        .home-title span {
          display: block;
          white-space: nowrap !important;
          word-break: keep-all !important;
          overflow-wrap: normal !important;
          hyphens: none !important;
        }
        .home-deck {
          color: var(--muted);
          font-size: clamp(1.02rem, 1.7vw, 1.52rem);
          font-weight: 700;
          line-height: 1.42;
          max-width: 760px;
          margin-bottom: 28px;
        }
        .home-folio {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 14px;
        }
        .home-folio div {
          border-top: 4px solid var(--dorado);
          padding-top: 10px;
        }
        .home-folio b {
          display: block;
          color: var(--guinda-dark);
          font-size: clamp(1.55rem, 2.8vw, 2.7rem);
          font-weight: 900;
          line-height: .92;
        }
        .home-folio span {
          display: block;
          color: var(--muted);
          font-size: .72rem;
          font-weight: 900;
          text-transform: uppercase;
          line-height: 1.18;
          margin-top: 7px;
        }
        .home-section {
          border-top: 6px solid var(--black);
          padding: 22px 0 30px;
          margin: 34px 0 28px;
          animation: editorialRise .52s ease both;
          transition: border-color .24s ease;
        }
        .home-section:hover { border-top-color: var(--guinda); }
        .home-section-head {
          display: grid;
          grid-template-columns: .8fr 1.2fr;
          gap: 26px;
          align-items: end;
          margin-bottom: 18px;
        }
        .home-section-head .label {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .home-section-head .title {
          color: var(--black);
          font-size: clamp(1.9rem, 3.6vw, 4.1rem);
          font-weight: 900;
          line-height: .9;
          text-transform: uppercase;
        }
        .home-section-head .body {
          color: var(--muted);
          font-size: 1rem;
          font-weight: 700;
          line-height: 1.45;
        }
        .home-doc-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 22px;
          margin-top: 18px;
        }
        .home-doc-card {
          border-top: 5px solid var(--guinda);
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          padding: 18px 0 0;
          box-shadow: 0 0 0 rgba(70,45,25,0);
          transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        }
        .home-doc-card:nth-child(2) { border-color: var(--verde); }
        .home-doc-card:hover {
          transform: translateY(-4px);
          border-color: var(--dorado);
          box-shadow: 0 18px 38px rgba(70,45,25,.1);
        }
        .home-doc-card b {
          display: block;
          color: var(--black);
          font-size: clamp(1.22rem, 2vw, 1.85rem);
          font-weight: 900;
          line-height: 1.02;
          text-transform: uppercase;
          margin-bottom: 12px;
        }
        .home-doc-card span {
          display: block;
          color: var(--muted);
          font-size: .95rem;
          font-weight: 700;
          line-height: 1.42;
        }
        .home-doc-card a {
          display: inline-block;
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
          text-decoration: none;
          border-bottom: 2px solid rgba(107,21,49,.32);
          margin-top: 14px;
        }
        .home-download-band {
          border-top: 5px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          padding: 18px 0 20px;
          margin: 8px 0 30px;
        }
        .reading-rail {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 18px;
          margin-top: 18px;
        }
        .reading-rail div {
          border-left: 6px solid var(--guinda);
          padding-left: 14px;
          min-height: 82px;
          animation: editorialRise .52s ease both;
        }
        .reading-rail div:nth-child(2) { border-color: var(--dorado); animation-delay: .08s; }
        .reading-rail div:nth-child(3) { border-color: var(--verde); animation-delay: .16s; }
        .reading-rail b {
          color: var(--guinda-dark);
          display: block;
          font-size: 1.35rem;
          font-weight: 900;
          line-height: .9;
          margin-bottom: 8px;
        }
        .reading-rail span {
          color: var(--muted);
          display: block;
          font-size: .86rem;
          font-weight: 750;
          line-height: 1.35;
        }
        .data-editorial-head {
          display: grid;
          grid-template-columns: .7fr 1.3fr;
          gap: 28px;
          align-items: end;
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          margin: 40px 0 20px;
          padding: 20px 0 22px;
          animation: editorialRise .48s ease both;
        }
        .data-editorial-head .label,
        .chart-kicker {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .data-editorial-head .title {
          color: var(--black);
          font-size: clamp(2.4rem, 5vw, 5.8rem);
          font-weight: 900;
          line-height: .86;
          text-transform: uppercase;
          margin-top: 8px;
        }
        .data-editorial-head p {
          color: var(--muted);
          font-size: clamp(1rem, 1.6vw, 1.35rem);
          font-weight: 700;
          line-height: 1.42;
          margin: 0;
        }
        .chart-kicker {
          border-top: 1px solid rgba(20,16,13,.18);
          margin-top: 22px;
          padding-top: 16px;
        }
        .analysis-reader {
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          margin: 38px 0 28px;
          padding: 20px 0 24px;
          animation: editorialRise .48s ease both;
        }
        .analysis-head {
          display: grid;
          grid-template-columns: .7fr 1.3fr;
          gap: 28px;
          align-items: end;
          margin-bottom: 20px;
        }
        .analysis-head .label {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .analysis-head .title {
          color: var(--black);
          font-size: clamp(2.35rem, 4.8vw, 5.3rem);
          font-weight: 900;
          line-height: .86;
          text-transform: uppercase;
          margin-top: 8px;
        }
        .analysis-head p {
          color: var(--muted);
          font-size: clamp(1rem, 1.55vw, 1.28rem);
          font-weight: 700;
          line-height: 1.42;
          margin: 0;
        }
        .analysis-grid {
          display: grid;
          grid-template-columns: 1.12fr .94fr .94fr;
          gap: 20px;
          margin: 18px 0 24px;
        }
        .analysis-card {
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          border-top: 5px solid var(--guinda);
          padding: 18px 0 0;
          animation: editorialRise .5s ease both;
          transition: transform .2s ease, border-color .2s ease;
        }
        .analysis-card:nth-child(2) { border-color: var(--dorado); animation-delay: .06s; }
        .analysis-card:nth-child(3) { border-color: var(--verde); animation-delay: .12s; }
        .analysis-card:hover { transform: translateY(-3px); border-color: var(--black); }
        .analysis-card b {
          color: var(--black);
          display: block;
          font-size: clamp(1.18rem, 1.8vw, 1.65rem);
          font-weight: 900;
          line-height: 1.02;
          text-transform: uppercase;
          margin-bottom: 10px;
        }
        .analysis-card p {
          color: var(--muted);
          font-size: .94rem;
          font-weight: 700;
          line-height: 1.45;
          margin: 0;
        }
        .analysis-split {
          display: grid;
          grid-template-columns: 1.24fr .76fr;
          gap: 24px;
          align-items: start;
        }
        .analysis-list {
          display: grid;
          gap: 10px;
          margin-top: 12px;
        }
        .analysis-row {
          display: grid;
          grid-template-columns: minmax(180px, 1fr) minmax(86px, auto) minmax(72px, auto);
          gap: 12px;
          align-items: baseline;
          border-top: 1px solid rgba(20,16,13,.18);
          padding-top: 10px;
          transition: background .18s ease, border-color .18s ease, transform .18s ease;
        }
        .analysis-row:hover {
          background: rgba(234,215,166,.16);
          border-top-color: var(--dorado);
          transform: translateX(3px);
        }
        .analysis-row span {
          color: var(--black);
          font-size: .84rem;
          font-weight: 900;
          line-height: 1.16;
          text-transform: uppercase;
        }
        .analysis-row b {
          color: var(--guinda-dark);
          font-size: 1.08rem;
          font-weight: 900;
          text-align: right;
          white-space: nowrap;
        }
        .analysis-row em {
          color: var(--muted);
          font-size: .68rem;
          font-style: normal;
          font-weight: 900;
          text-align: right;
          text-transform: uppercase;
        }
        .analysis-note {
          border-left: 7px solid var(--dorado);
          background: rgba(251,242,229,.55);
          padding: 15px 0 15px 18px;
        }
        .analysis-note b {
          color: var(--guinda-dark);
          display: block;
          font-size: .88rem;
          font-weight: 900;
          text-transform: uppercase;
          margin-bottom: 8px;
        }
        .analysis-note span {
          color: var(--muted);
          display: block;
          font-size: .9rem;
          font-weight: 700;
          line-height: 1.42;
        }
        .viz-section {
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.24);
          margin: 32px 0 26px;
          padding: 20px 0 22px;
          animation: editorialRise .48s ease both;
        }
        .viz-head {
          display: grid;
          grid-template-columns: .72fr 1.28fr;
          gap: 28px;
          align-items: end;
          margin-bottom: 18px;
        }
        .viz-head .label {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .viz-head .title {
          color: var(--black);
          font-size: clamp(2rem, 4vw, 4.4rem);
          font-weight: 900;
          line-height: .88;
          text-transform: uppercase;
          margin-top: 8px;
        }
        .viz-head p {
          color: var(--muted);
          font-size: 1rem;
          font-weight: 700;
          line-height: 1.42;
          margin: 0;
        }
        .sanction-extremes {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 18px;
          margin: 18px 0 20px;
        }
        .sanction-extremes div {
          border-top: 5px solid var(--guinda);
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          padding: 16px 0 0;
          animation: editorialRise .54s ease both;
        }
        .sanction-extremes div:nth-child(2) { border-color: var(--dorado); animation-delay: .08s; }
        .sanction-extremes span {
          color: var(--muted);
          display: block;
          font-size: .68rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .sanction-extremes b {
          color: var(--black);
          display: block;
          font-size: clamp(1.05rem, 1.8vw, 1.55rem);
          font-weight: 900;
          line-height: 1.04;
          margin-top: 8px;
          text-transform: uppercase;
        }
        .sanction-extremes strong {
          color: var(--guinda-dark);
          display: block;
          font-size: clamp(2rem, 3.4vw, 3rem);
          font-weight: 900;
          line-height: .9;
          margin-top: 10px;
        }
        .sanction-extremes em {
          color: var(--muted);
          display: block;
          font-size: .78rem;
          font-style: normal;
          font-weight: 850;
          margin-top: 8px;
          text-transform: uppercase;
        }
        .expedient-table-wrap {
          border-top: 6px solid var(--guinda);
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          margin: 14px 0 24px;
          overflow-x: auto;
          box-shadow: 0 16px 34px rgba(70,45,25,.08);
          animation: editorialRise .5s ease both;
        }
        .expedient-table {
          width: 100%;
          min-width: 940px;
          border-collapse: collapse;
        }
        .expedient-table th {
          background: var(--guinda);
          color: #fffdf8;
          font-size: .68rem;
          font-weight: 900;
          line-height: 1.1;
          padding: 12px 12px;
          text-align: left;
          text-transform: uppercase;
          white-space: nowrap;
        }
        .expedient-table th:nth-child(5),
        .expedient-table td.money-cell { text-align: right; }
        .expedient-table td {
          border-bottom: 1px solid rgba(20,16,13,.16);
          color: var(--muted);
          font-size: .78rem;
          font-weight: 750;
          line-height: 1.32;
          padding: 13px 12px;
          vertical-align: top;
        }
        .expedient-table tbody tr:nth-child(even) td { background: rgba(234,215,166,.16); }
        .expedient-table tbody tr:hover td { background: rgba(107,21,49,.07); }
        .expedient-table a {
          color: var(--guinda);
          font-weight: 900;
          text-decoration: none;
          border-bottom: 1px solid rgba(107,21,49,.38);
        }
        .exp-id {
          color: var(--black) !important;
          font-weight: 900 !important;
          min-width: 180px;
        }
        .exp-id span,
        .money-cell span {
          color: var(--muted);
          display: block;
          font-size: .68rem;
          font-weight: 850;
          margin-top: 5px;
          text-transform: uppercase;
        }
        .money-cell {
          color: var(--guinda-dark) !important;
          font-size: 1rem !important;
          font-weight: 900 !important;
          white-space: nowrap;
        }
        .status-pill {
          background: var(--guinda);
          border-radius: 999px;
          color: #fffdf8;
          display: inline-flex;
          font-size: .64rem;
          font-weight: 900;
          line-height: 1.05;
          padding: 7px 10px;
          text-transform: uppercase;
        }
        .expedient-empty {
          border-top: 5px solid var(--dorado);
          background: #fffdf8;
          color: var(--guinda-dark);
          font-size: 1rem;
          font-weight: 900;
          padding: 18px 0;
          text-transform: uppercase;
        }
        .expedient-empty strong {
          color: var(--guinda-dark);
          font-weight: 900;
        }
        .home-panel-anchor { display: block; height: 1px; scroll-margin-top: 90px; }
        @keyframes editorialRise {
          from { opacity: 0; transform: translateY(14px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes editorialFocus {
          from { opacity: 0; transform: translateY(18px) scale(.985); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes statePulse {
          0%, 100% { filter: drop-shadow(0 0 0 rgba(107,21,49,0)); }
          50% { filter: drop-shadow(0 0 7px rgba(107,21,49,.42)); }
        }
        @keyframes dockFloat {
          from { opacity: 0; transform: translateY(18px) scale(.98); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @supports (animation-timeline: view()) {
          .home-section,
          .analysis-reader,
          .criteria-reader,
          .data-editorial-head,
          .viz-section,
          .responsive-kpi,
          .expedient-table-wrap,
          .stPlotlyChart {
            animation-name: editorialRise;
            animation-duration: 1ms;
            animation-fill-mode: both;
            animation-timeline: view();
            animation-range: entry 8% cover 24%;
          }
        }
        .meeting-brief {
          display: grid;
          grid-template-columns: .78fr 1.22fr;
          gap: 28px;
          align-items: start;
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          padding: 18px 0 20px;
          margin: 18px 0 30px;
        }
        .meeting-copy .label { color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; }
        .meeting-copy .title { color: var(--black); font-size: clamp(1.9rem, 3vw, 3.6rem); font-weight: 900; line-height: .92; text-transform: uppercase; margin: 8px 0 12px; }
        .meeting-copy p { color: var(--muted); font-size: .98rem; font-weight: 650; line-height: 1.45; }
        .meeting-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 14px;
        }
        .meeting-grid div { border-top: 4px solid var(--dorado); padding-top: 10px; }
        .meeting-grid b {
          display: block;
          color: var(--guinda-dark);
          font-size: .86rem;
          font-weight: 900;
          text-transform: uppercase;
          line-height: 1.18;
          margin-bottom: 6px;
        }
        .meeting-grid span {
          display: block;
          color: var(--muted);
          font-size: .86rem;
          font-weight: 650;
          line-height: 1.38;
        }
        .meeting-flow {
          grid-column: 1 / -1;
          display: grid;
          grid-template-columns: repeat(5, minmax(110px, 1fr));
          gap: 10px;
          align-items: center;
          margin-top: 6px;
        }
        .meeting-flow span {
          border: 1px solid var(--line);
          background: #fffdf8;
          color: var(--guinda-dark);
          padding: 10px 12px;
          font-size: .74rem;
          font-weight: 900;
          text-transform: uppercase;
          text-align: center;
        }
        .meeting-flow i { display: none; }
        .map-deck {
          display: grid;
          grid-template-columns: .72fr 1.28fr;
          gap: 32px;
          align-items: start;
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          padding: 18px 0 20px;
          margin: 26px 0 18px;
        }
        .map-copy .label { color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; }
        .map-copy .title { color: var(--black); font-size: clamp(2rem, 3.5vw, 4.3rem); font-weight: 900; line-height: .88; text-transform: uppercase; margin: 8px 0 12px; }
        .map-copy .body { color: var(--muted); font-size: 1rem; font-weight: 650; line-height: 1.45; }
        .mexico-map-wrap {
          position: relative;
          border-top: 4px solid var(--guinda);
          border-bottom: 1px solid rgba(20,16,13,.25);
          background: #fbf7ef;
          min-height: 390px;
          overflow: hidden;
        }
        .map-svg {
          width: 100%;
          height: 390px;
          display: block;
        }
        .state {
          fill: #e8ddcc;
          stroke: #fffdf8;
          stroke-width: 2.2;
          vector-effect: non-scaling-stroke;
        }
        .state.active {
          fill: var(--guinda);
          stroke: #fffdf8;
          animation: statePulse 2.8s ease-in-out infinite;
        }
        .state.linked { cursor: pointer; transition: fill .18s ease, opacity .18s ease, filter .18s ease; }
        a:hover .state.linked,
        .state.linked:hover {
          fill: var(--dorado);
          filter: drop-shadow(0 5px 8px rgba(107,21,49,.28));
          opacity: .96;
        }
        .map-notes {
          position: absolute;
          right: 18px;
          top: 20px;
          display: grid;
          gap: 8px;
          width: 190px;
        }
        .map-note {
          background: rgba(255,253,248,.9);
          border-left: 4px solid var(--guinda);
          color: inherit;
          display: block;
          padding: 8px 10px;
          text-decoration: none;
          transition: transform .18s ease, border-color .18s ease, background .18s ease;
        }
        .map-note:hover { background: #fffdf8; border-color: var(--dorado); transform: translateX(-2px); }
        .map-note strong {
          display: block;
          color: var(--guinda-dark);
          font-size: .74rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .map-note span {
          display: block;
          color: var(--muted);
          font-size: .65rem;
          font-weight: 900;
          text-transform: uppercase;
          margin-top: 2px;
        }
        .incidence-card-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 16px;
          margin-top: 18px;
        }
        .incidence-card {
          border-top: 5px solid var(--guinda);
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          padding: 14px 0 0;
          scroll-margin-top: 100px;
          animation: editorialRise .5s ease both;
        }
        .incidence-card strong {
          color: var(--black);
          display: block;
          font-size: 1.1rem;
          font-weight: 900;
          line-height: 1;
          text-transform: uppercase;
          margin-bottom: 10px;
        }
        .incidence-card-entry {
          border-top: 1px solid rgba(20,16,13,.18);
          padding: 10px 0 12px;
        }
        .incidence-card-entry b {
          color: var(--guinda-dark);
          display: block;
          font-size: .86rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .incidence-card-entry span {
          color: var(--black);
          display: block;
          font-size: .78rem;
          font-weight: 900;
          line-height: 1.24;
          margin-top: 5px;
        }
        .incidence-card-entry p {
          color: var(--muted);
          font-size: .78rem;
          font-weight: 700;
          line-height: 1.35;
          margin: 6px 0 8px;
        }
        .incidence-card-entry a {
          color: var(--guinda);
          font-size: .72rem;
          font-weight: 900;
          text-decoration: none;
          text-transform: uppercase;
          border-bottom: 1px solid rgba(107,21,49,.36);
        }
        .incidence-card-grid:has(.incidence-card:target) {
          grid-template-columns: minmax(0, 1fr);
        }
        .incidence-card-grid:has(.incidence-card:target) .incidence-card:not(:target) {
          display: none;
        }
        .incidence-card:target {
          border-top-color: var(--dorado);
          box-shadow: 0 18px 44px rgba(70,45,25,.14);
          animation: editorialFocus .42s cubic-bezier(.2,.8,.2,1) both;
        }
        .incidence-close {
          border: 1px solid rgba(107,21,49,.25);
          border-radius: 999px;
          color: var(--guinda-dark);
          display: inline-flex;
          font-size: .64rem;
          font-weight: 900;
          margin: 0 0 12px;
          padding: 7px 10px;
          text-decoration: none;
          text-transform: uppercase;
          transition: background .18s ease, color .18s ease, border-color .18s ease;
        }
        .incidence-close:hover {
          background: var(--guinda);
          border-color: var(--guinda);
          color: #fffdf8;
        }
        .incidence-strip {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 14px;
          margin-top: 18px;
        }
        .incidence-strip div {
          border-top: 3px solid var(--dorado);
          padding-top: 8px;
        }
        .incidence-strip strong {
          display: block;
          color: var(--guinda-dark);
          font-size: clamp(1.7rem, 3vw, 2.6rem);
          font-weight: 900;
          line-height: .9;
        }
        .incidence-strip span {
          display: block;
          color: var(--muted);
          font-size: .66rem;
          font-weight: 900;
          line-height: 1.1;
          margin-top: 7px;
          text-transform: uppercase;
        }
        .incidence-list {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 18px;
          margin: 0 0 28px;
        }
        .incidence-item {
          border-top: 1px solid rgba(20,16,13,.22);
          padding-top: 12px;
        }
        .incidence-item strong {
          display: block;
          color: var(--guinda-dark);
          font-size: .9rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .incidence-item span {
          display: block;
          color: var(--black);
          font-size: .78rem;
          font-weight: 900;
          margin: 5px 0;
        }
        .incidence-item em {
          display: block;
          color: var(--muted);
          font-size: .78rem;
          font-style: normal;
          font-weight: 650;
          line-height: 1.35;
        }
        .incidence-entry {
          margin-top: 10px;
        }
        .incidence-entry b {
          display: block;
          color: var(--black);
          font-size: .78rem;
          line-height: 1.2;
        }
        .incidence-entry em {
          display: block;
          color: var(--muted);
          font-size: .75rem;
          font-style: normal;
          font-weight: 650;
          line-height: 1.34;
          margin-top: 4px;
        }
        .link-list {
          display: grid;
          gap: 14px;
          margin: 14px 0 28px;
        }
        .method-separator {
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.22);
          margin: 16px 0 12px;
          padding: 14px 0;
        }
        .method-separator strong {
          display: block;
          color: var(--guinda-dark);
          font-size: .86rem;
          font-weight: 900;
          text-transform: uppercase;
          margin-bottom: 6px;
        }
        .method-separator span {
          display: block;
          color: var(--muted);
          font-size: .9rem;
          font-weight: 650;
          line-height: 1.42;
          max-width: 980px;
        }
        .method-separator p {
          color: var(--muted);
          font-size: .9rem;
          font-weight: 650;
          line-height: 1.42;
          margin: 0 0 12px;
          max-width: 980px;
        }
	        .method-grid {
	          display: grid;
	          grid-template-columns: repeat(2, minmax(0, 1fr));
	          gap: 18px 24px;
	        }
        .method-grid div {
          border-top: 3px solid var(--dorado);
          padding-top: 8px;
        }
        .method-grid b {
          display: block;
          color: var(--guinda-dark);
          font-size: .86rem;
          font-weight: 900;
          line-height: 1.18;
        }
        .method-grid span {
          font-size: .8rem;
          line-height: 1.34;
          margin-top: 5px;
        }
        .link-item {
          display: grid;
          grid-template-columns: minmax(150px, .35fr) minmax(120px, .25fr) minmax(260px, 1fr) minmax(160px, .35fr);
          gap: 18px;
          align-items: start;
          border-top: 1px solid rgba(20,16,13,.22);
          padding-top: 14px;
        }
        .link-item .case-id { color: var(--guinda-dark); font-weight: 900; text-transform: uppercase; }
        .link-item .case-geo {
          color: var(--black);
          font-size: .78rem;
          font-weight: 900;
          line-height: 1.25;
          text-transform: uppercase;
        }
        .link-item .case-geo span {
          display: block;
          color: var(--muted);
          font-weight: 800;
          margin-top: 4px;
        }
        .link-item .case-text { color: var(--muted); font-weight: 650; line-height: 1.36; }
        .link-item a {
          color: var(--guinda);
          font-size: .76rem;
          font-weight: 900;
          text-align: right;
          text-decoration: none;
          overflow-wrap: anywhere;
          word-break: break-word;
        }
        .link-item a:hover { text-decoration: underline; }
        .story-hero {
          display: grid;
          grid-template-columns: 1.08fr .92fr;
          gap: 28px;
          align-items: stretch;
          margin: 26px 0 18px;
          padding: 12px 0 22px;
          border-bottom: 1px solid rgba(20,16,13,.28);
        }
        .story-card {
          position: relative;
          overflow: hidden;
          background: transparent;
          border: 0;
          border-left: 7px solid var(--dorado);
          padding: 4px 0 4px 18px;
          min-height: 148px;
          box-shadow: none;
        }
        .story-card.majority {
          background:
            linear-gradient(90deg, rgba(107,21,49,.12), transparent 62%);
          border-left-color: var(--guinda);
          color: var(--ink);
          padding: 16px 0 16px 24px;
        }
        .story-card.majority .story-label,
        .story-card.majority .story-note { color: var(--muted); }
        .story-card.majority .story-number { color: var(--guinda-dark); }
        .story-label { color: var(--guinda); font-size: .78rem; font-weight: 900; text-transform: uppercase; }
        .story-number { color: var(--guinda-dark); font-size: clamp(3rem, 6vw, 6.8rem); font-weight: 900; line-height: .82; margin-top: 10px; }
        .story-note { color: var(--muted); font-weight: 700; line-height: 1.35; max-width: 560px; }
        .story-split { display: grid; grid-template-columns: repeat(2, 1fr); gap: 22px; align-content: center; }
        .case-ribbon {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 22px;
          background: transparent;
          border: 0;
          border-top: 5px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          margin: 20px 0 28px;
          padding: 16px 0;
        }
        .case-ribbon div {
          background: transparent;
          border-left: 4px solid var(--dorado);
          padding: 0 0 0 14px;
          min-height: 72px;
        }
        .case-ribbon strong { display: block; color: var(--guinda-dark); font-size: 2.1rem; line-height: .9; font-weight: 900; }
        .case-ribbon span { display: block; color: var(--muted); font-size: .7rem; font-weight: 900; text-transform: uppercase; margin-top: 8px; }
        .databox { border-top: 4px solid var(--black); padding-top: 8px; background: rgba(241,234,223,.7); }
        .databox strong { display:block; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 2rem; color: var(--guinda); }
        .verdict-ok { border-left: 5px solid var(--verde); padding: 10px 12px; background: #f6f1e8; }
        .verdict-warn { border-left: 5px solid var(--dorado); padding: 10px 12px; background: #f6f1e8; }
        .rule { border-top: 1px solid var(--black); margin: 16px 0; }
        .portrait-grid { display: grid; grid-template-columns: repeat(2, minmax(260px, 1fr)); gap: 18px; margin: 12px 0 20px; }
        .portrait-card { background: rgba(255,250,241,.96); border-top: 5px solid var(--guinda); border-bottom: 1px solid var(--line); display: grid; grid-template-columns: 132px 1fr; gap: 14px; padding: 12px; }
        .portrait-card img { width: 132px; aspect-ratio: 4/5; object-fit: cover; border: 1px solid var(--line); filter: saturate(.94) contrast(1.03); }
        .portrait-card .name { font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 1.12rem; line-height: 1.05; color: var(--black); text-transform: uppercase; }
        .portrait-card .meta { color: var(--muted); font-size: .86rem; line-height: 1.35; margin-top: 6px; }
        .portrait-card .status { color: var(--verde); font-weight: 800; text-transform: uppercase; font-size: .72rem; margin-top: 8px; }
        .dataviz-band {
          background: transparent;
          border-top: 3px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.2);
          padding: 14px 0 18px;
          margin: 8px 0 18px;
        }
        .section-label { color: var(--guinda); font-weight: 900; font-size: .78rem; text-transform: uppercase; letter-spacing: 0; }
        .summary-strip { display: grid; grid-template-columns: 1.05fr .95fr; gap: 18px; margin: 18px 0; }
        .kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; margin: 20px 0 26px; }
        .kpi-tile {
          background: transparent;
          border: 0;
          border-left: 5px solid var(--guinda);
          padding: 4px 0 4px 14px;
          min-height: 78px;
          box-shadow: none;
        }
        .kpi-tile .kpi-label { color: var(--muted); font-size: .68rem; font-weight: 900; text-transform: uppercase; line-height: 1.05; }
        .kpi-tile .kpi-value { color: var(--guinda-dark); font-size: clamp(2rem, 3vw, 3.05rem); font-weight: 900; line-height: .95; margin-top: 12px; }
        .composition-card {
          background: rgba(255,253,248,.46);
          border: 0;
          border-top: 4px solid var(--guinda);
          padding: 14px 0 0;
        }
        .composition-title { font-size: .78rem; font-weight: 900; color: var(--guinda); text-transform: uppercase; margin-bottom: 10px; }
        .party-row { display: grid; grid-template-columns: 72px 1fr 42px; align-items: center; gap: 10px; margin: 8px 0; }
        .party-row .party { font-weight: 900; color: var(--black); }
        .party-row .bar { height: 12px; background: #e6d8c6; overflow: hidden; }
        .party-row .fill { height: 100%; background: var(--guinda); }
        .party-row .value { font-weight: 900; text-align: right; color: var(--guinda-dark); }
        .tight-grid { display: grid; grid-template-columns: repeat(6, minmax(118px, 1fr)); gap: 12px; }
        .mini-portrait {
          position: relative;
          overflow: hidden;
          background: transparent;
          border: 0;
          border-top: 4px solid var(--guinda);
          padding: 7px 0 0;
          min-height: 242px;
          box-shadow: none;
        }
        .mini-portrait:before { content: ""; position: absolute; inset: 0; background: transparent; pointer-events: none; }
        .mini-portrait img { position: relative; width: 100%; aspect-ratio: 4/5; object-fit: cover; filter: grayscale(1) contrast(1.12); border-bottom: 4px solid var(--guinda); }
        .mini-portrait .mini-name { position: relative; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: .78rem; line-height: 1.08; margin-top: 7px; color: var(--black); text-transform: uppercase; }
        .mini-portrait .mini-meta { position: relative; color: var(--muted); font-size: .68rem; font-weight: 600; margin-top: 4px; }
        .criteria-reader {
          border-top: 6px solid var(--black);
          border-bottom: 1px solid rgba(20,16,13,.28);
          margin: 24px 0 30px;
          padding: 18px 0 20px;
        }
        .criteria-reader .reader-head {
          display: grid;
          grid-template-columns: .74fr 1.26fr;
          gap: 28px;
          align-items: end;
          margin-bottom: 18px;
        }
        .criteria-reader .label {
          color: var(--guinda);
          font-size: .78rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .criteria-reader .title {
          color: var(--black);
          font-size: clamp(2.05rem, 3.8vw, 4.6rem);
          font-weight: 900;
          line-height: .9;
          text-transform: uppercase;
          margin-top: 8px;
        }
        .criteria-reader .body {
          color: var(--muted);
          font-size: 1rem;
          font-weight: 650;
          line-height: 1.46;
          max-width: 760px;
        }
        .criteria-map {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 12px;
          margin: 16px 0 20px;
        }
        .criteria-map a {
          display: block;
          border-top: 4px solid var(--dorado);
          color: var(--guinda-dark);
          text-decoration: none;
          padding-top: 8px;
          min-height: 64px;
        }
        .criteria-map a:hover { border-color: var(--guinda); transform: translateY(-2px); transition: transform .18s ease, border-color .18s ease; }
        .criteria-map b {
          display: block;
          color: var(--guinda);
          font-size: .86rem;
          font-weight: 900;
          line-height: 1;
        }
        .criteria-map span {
          display: block;
          color: var(--muted);
          font-size: .72rem;
          font-weight: 850;
          line-height: 1.16;
          margin-top: 6px;
          text-transform: uppercase;
        }
        .criteria-lanes {
          display: grid;
          grid-template-columns: 1.05fr .95fr;
          gap: 22px;
          align-items: start;
        }
        .criteria-stack {
          display: grid;
          gap: 12px;
        }
        .criterion-detail {
          border-top: 4px solid var(--guinda);
          background: linear-gradient(180deg, rgba(255,253,248,.86), rgba(251,242,229,.56));
          padding: 0;
          transition: background .2s ease, border-color .2s ease, box-shadow .2s ease, transform .2s ease;
        }
        .criterion-detail:nth-child(3n+2) { border-top-color: var(--dorado); }
        .criterion-detail:nth-child(3n+3) { border-top-color: var(--verde); }
        .criterion-detail:hover {
          box-shadow: 0 14px 30px rgba(70,45,25,.08);
          transform: translateY(-2px);
        }
        .criterion-detail[open] {
          background: #fffdf8;
          box-shadow: 0 18px 36px rgba(70,45,25,.1);
        }
        .criterion-detail summary {
          list-style: none;
          cursor: pointer;
          display: grid;
          grid-template-columns: .62in 1fr auto;
          gap: 14px;
          align-items: baseline;
          padding: 13px 0 12px;
        }
        .criterion-detail summary::-webkit-details-marker { display: none; }
        .criterion-detail summary b {
          color: var(--guinda);
          font-size: .9rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .criterion-detail summary strong {
          color: var(--black);
          font-size: 1.05rem;
          font-weight: 900;
          line-height: 1.12;
        }
        .criterion-detail summary span {
          color: var(--muted);
          font-size: .7rem;
          font-weight: 900;
          text-transform: uppercase;
          text-align: right;
        }
        [data-testid="stExpander"] {
          border: 0;
          border-top: 4px solid var(--guinda);
          border-radius: 0;
          background: linear-gradient(180deg, rgba(255,253,248,.88), rgba(251,242,229,.54));
          box-shadow: none;
          margin-bottom: 12px;
          transition: background .2s ease, border-color .2s ease, transform .18s ease;
        }
        [data-testid="stExpander"]:nth-of-type(3n+2) { border-top-color: var(--dorado); }
        [data-testid="stExpander"]:nth-of-type(3n+3) { border-top-color: var(--verde); }
        [data-testid="stExpander"]:hover { transform: translateY(-1px); }
        [data-testid="stExpander"] details {
          border: 0 !important;
          border-radius: 0 !important;
          background: transparent !important;
        }
        [data-testid="stExpander"] summary {
          padding: 13px 0 12px !important;
        }
        [data-testid="stExpander"] summary p {
          color: var(--black) !important;
          font-size: 1.02rem !important;
          font-weight: 900 !important;
          line-height: 1.12 !important;
        }
        .criterion-body {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px 24px;
          padding: 0 0 16px .62in;
          animation: criteriaReveal .22s ease both;
        }
        .streamlit-criterion { padding-left: 0; }
        @keyframes criteriaReveal {
          from { opacity: 0; transform: translateY(-4px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .criterion-field {
          border-top: 1px solid rgba(20,16,13,.24);
          padding-top: 8px;
        }
        .criterion-field.rule { grid-column: 1 / -1; border-top: 3px solid var(--black); }
        .criterion-field.utility { grid-column: 1 / -1; }
        .criterion-field label {
          display: block;
          color: var(--guinda);
          font-size: .72rem;
          font-weight: 900;
          line-height: 1.14;
          text-transform: uppercase;
          margin-bottom: 5px;
        }
        .criterion-field p {
          color: var(--muted);
          font-size: .9rem;
          font-weight: 650;
          line-height: 1.4;
          margin: 0;
        }
        .criterion-field.rule p {
          color: var(--black);
          font-style: italic;
          font-weight: 800;
          text-decoration: underline;
          text-decoration-thickness: 1px;
          text-underline-offset: 3px;
        }
        .criterion-field .source-links {
          display: flex;
          flex-wrap: wrap;
          gap: 8px 14px;
        }
        .criterion-field .source-links a {
          color: var(--guinda);
          font-size: .82rem;
          font-weight: 900;
          text-decoration: none;
          border-bottom: 1px solid rgba(107,21,49,.42);
        }
        .criteria-timeline {
          position: sticky;
          top: 18px;
          display: grid;
          gap: 12px;
          border-top: 5px solid var(--black);
          padding-top: 12px;
        }
        .timeline-card {
          border-left: 6px solid var(--guinda);
          padding-left: 14px;
        }
        .timeline-card:nth-child(2) { border-color: var(--dorado); }
        .timeline-card:nth-child(3) { border-color: var(--verde); }
        .timeline-card b {
          display: block;
          color: var(--guinda-dark);
          font-size: .86rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .timeline-card span {
          display: block;
          color: var(--muted);
          font-size: .84rem;
          font-weight: 650;
          line-height: 1.36;
          margin-top: 6px;
        }
        .reader-filter-note {
          color: var(--muted);
          font-size: .8rem;
          font-weight: 750;
          line-height: 1.3;
          margin: -4px 0 14px;
        }
        .section-subhead {
          border-top: 6px solid var(--black);
          color: var(--black);
          font-size: clamp(1.9rem, 3.2vw, 3.9rem);
          font-weight: 900;
          line-height: .9;
          margin: 28px 0 18px;
          padding-top: 12px;
          text-transform: uppercase;
        }
        .executive-reading {
          border-bottom: 1px solid rgba(20,16,13,.24);
          margin: 22px 0 28px;
          padding-bottom: 20px;
        }
        .executive-reading p {
          color: var(--muted);
          font-size: clamp(1rem, 1.45vw, 1.2rem);
          font-weight: 750;
          line-height: 1.48;
          max-width: 1060px;
        }
        .executive-reading strong {
          color: var(--black);
          font-weight: 900;
        }
        .methodology-band {
          border-top: 6px solid var(--guinda);
          border-bottom: 1px solid rgba(20,16,13,.24);
          margin: 32px 0 28px;
          padding: 20px 0 24px;
          animation: editorialRise .52s ease both;
        }
        .methodology-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 18px;
          margin-top: 20px;
        }
        .methodology-grid article {
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          border-top: 4px solid var(--dorado);
          padding: 14px 0 0;
          transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        }
        .methodology-grid article:hover {
          border-top-color: var(--guinda);
          box-shadow: 0 16px 34px rgba(70,45,25,.1);
          transform: translateY(-3px);
        }
        .methodology-grid b {
          color: var(--guinda-dark);
          display: block;
          font-size: .9rem;
          font-weight: 900;
          line-height: 1.1;
          text-transform: uppercase;
        }
        .methodology-grid p {
          color: var(--muted);
          font-size: .86rem;
          font-weight: 720;
          line-height: 1.42;
          margin: 8px 0 0;
        }
        div[data-baseweb="select"] > div { border-radius: 0; border: 1px solid var(--line); background: #fffdf8; min-height: 46px; }
        .filter-band {
          border-top: 5px solid var(--guinda);
          background: linear-gradient(180deg, #fffdf8, #fbf2e5);
          margin: 14px 0 12px;
          padding: 14px 0 2px;
        }
        .filter-band .label {
          color: var(--guinda);
          font-size: .72rem;
          font-weight: 900;
          text-transform: uppercase;
        }
        .filter-band .title {
          color: var(--black);
          font-size: clamp(1.45rem, 2.4vw, 2.4rem);
          font-weight: 900;
          line-height: .95;
          text-transform: uppercase;
          margin-top: 4px;
        }
        .filter-band p {
          color: var(--muted);
          font-size: .82rem;
          font-weight: 750;
          line-height: 1.35;
          margin: 8px 0 4px;
        }
        [data-testid="stPills"] button {
          background: #fffdf8 !important;
          border: 1.5px solid rgba(107,21,49,.82) !important;
          border-radius: 999px !important;
          color: var(--guinda) !important;
          font-weight: 900 !important;
          text-transform: uppercase !important;
          transition: background .18s ease, color .18s ease, border-color .18s ease, transform .18s ease;
        }
        [data-testid="stPills"] button * {
          color: inherit !important;
        }
        [data-testid="stPills"] button:hover {
          border-color: var(--guinda) !important;
          transform: translateY(-1px);
        }
        [data-testid="stPills"] button[aria-pressed="true"],
        [data-testid="stPills"] button[aria-selected="true"],
        [data-testid="stPills"] button[aria-checked="true"],
        [data-testid="stPills"] button[data-selected="true"],
        [data-testid="stPills"] [role="option"][aria-selected="true"],
        [data-testid="stPills"] [role="checkbox"][aria-checked="true"] {
          background: var(--guinda) !important;
          border-color: var(--guinda) !important;
          color: #fffdf8 !important;
        }
        @media (min-width: 1181px) {
          .block-container { max-width: 1280px; }
          .map-deck { grid-template-columns: .64fr 1.36fr; }
        }
        @media (max-width: 900px) {
          .site-nav { align-items: flex-start; flex-direction: column; }
          .site-links { justify-content: flex-start; }
          .intro-lede, .sanction-board, .plain-steps, .meeting-brief, .meeting-grid, .map-deck, .link-item, .editorial-grid, .summary-strip, .story-hero, .story-split, .criteria-reader .reader-head, .criteria-lanes, .home-hero, .home-section-head, .home-doc-grid, .data-editorial-head, .reading-rail, .analysis-head, .analysis-grid, .analysis-split, .viz-head, .sanction-extremes, .methodology-grid { grid-template-columns: 1fr; }
          .link-item a { text-align: left; }
          .case-ribbon, .kpi-grid, .incidence-list, .criteria-map, .incidence-card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .masthead .headline { font-size: 2.5rem; }
          .criteria-timeline { position: static; grid-template-columns: 1fr; }
        }
        @media (max-width: 640px) {
          .block-container { padding-top: 1rem; padding-left: .9rem; padding-right: .9rem; }
          .block-container:before { height: 5px; margin-bottom: 14px; }
          .site-links { gap: 12px; }
          .site-links a { font-size: .66rem; }
          .download-dock {
            left: .75rem;
            right: .75rem;
            bottom: .75rem;
            justify-content: space-between;
          }
          .download-dock span { display: none; }
          .download-dock .pill { flex: 1; min-height: 42px; padding: 0 10px; }
          .intro-lede { gap: 16px; margin-top: 16px; }
          .intro-title { font-size: clamp(2rem, 13vw, 3.35rem); line-height: 1; }
          .intro-copy { font-size: .96rem; }
          .sanction-total .amount { font-size: clamp(2.6rem, 15vw, 4.1rem); }
          .cause-row { grid-template-columns: 1fr; gap: 5px; }
          .cause-row .money { text-align: left; font-size: 1.1rem; }
          .incidence-strip, .case-ribbon, .kpi-grid, .incidence-list, .meeting-flow, .tight-grid, .criteria-map, .criterion-body, .criteria-timeline, .home-folio { grid-template-columns: 1fr; }
          .home-hero { min-height: 0; padding-top: 24px; }
          .home-title { font-size: clamp(2.72rem, 13vw, 4.5rem); }
          .home-title span { white-space: normal; }
          .responsive-kpi-grid { grid-template-columns: 1fr; }
          .responsive-kpi { min-height: 124px; padding: 16px 14px; }
          .responsive-kpi .kpi-label { font-size: .64rem; }
          .responsive-kpi .kpi-value { font-size: clamp(2.15rem, 14vw, 3rem); }
          .responsive-kpi .kpi-value.money { font-size: clamp(2rem, 12vw, 2.8rem); }
          .data-editorial-head .title { font-size: clamp(2.2rem, 12vw, 3.6rem); line-height: .9; }
          .analysis-head .title { font-size: clamp(2.2rem, 12vw, 3.45rem); line-height: .9; }
          .analysis-row { grid-template-columns: 1fr; gap: 4px; }
          .analysis-row b,
          .analysis-row em { text-align: left; }
          .viz-head .title { font-size: clamp(2.1rem, 11vw, 3.25rem); }
          .expedient-table-wrap { margin-left: -.9rem; margin-right: -.9rem; border-top-width: 5px; }
          .expedient-table th,
          .expedient-table td { padding: 11px 10px; }
          .map-notes { position: static; width: auto; padding: 10px; }
          .incidence-card-grid { grid-template-columns: 1fr; }
          .criterion-detail summary { grid-template-columns: 48px 1fr; gap: 10px; }
          .criterion-detail summary span { grid-column: 1 / -1; text-align: left; }
          .criterion-body { padding-left: 0; }
          .map-copy .title { font-size: clamp(2rem, 11vw, 3rem); line-height: .94; }
          .link-item { gap: 8px; }
        }
        @page { size: letter landscape; margin: 0.42in; }
        @media print {
          html, body, .stApp { background: white !important; }
          div[data-testid="stSidebar"], header, footer, [data-testid="stToolbar"], .stDeployButton, button { display: none !important; }
          .block-container { padding: 0 !important; max-width: none !important; }
          h1 { font-size: 22pt !important; }
          h2 { font-size: 14pt !important; margin-top: 12pt !important; }
          h3 { font-size: 11pt !important; }
          p, li, div, span { font-size: 9pt; }
          [data-testid="stMetric"] { break-inside: avoid; border: 1px solid #b8a892 !important; }
          .element-container { break-inside: avoid; }
          .newspaper-shell { border: 0; padding: 0; }
          .portrait-grid { grid-template-columns: repeat(2, 1fr); gap: 10pt; }
          .portrait-card { break-inside: avoid; grid-template-columns: 96px 1fr; padding: 8pt; }
          .portrait-card img { width: 96px; }
          .tight-grid { grid-template-columns: repeat(6, 1fr); gap: 6pt; }
          .mini-portrait { padding: 5pt; min-height: auto; break-inside: avoid; }
          .story-hero { grid-template-columns: 1.1fr .9fr; gap: 8pt; }
          .case-ribbon { grid-template-columns: repeat(4, 1fr); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def mvp_notice() -> None:
    st.markdown(
        '<div class="notice"><strong>Corte de trabajo - diputaciones federales 2024.</strong> '
        "Corpus con sentencias oficiales localizadas, fichas públicas de Cámara y verificación nominal documentada. "
        "Las consultas de sanciones se reportan por fuente y alcance.</div>",
        unsafe_allow_html=True,
    )


def format_money(value: float | int | str) -> str:
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"
