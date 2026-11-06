import re
from html import escape

import streamlit as st


st.set_page_config(
    page_title="Beyond Earth — Rockets & Missions",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROCKETS = {
    "Saturn V": {
        "image": "https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&w=1500&q=90",
        "era": "UNITED STATES · 1967–1973",
        "short": "The towering launch vehicle that sent Apollo crews toward the Moon.",
        "facts": ["CREWED LUNAR FLIGHTS", "APOLLO PROGRAM"],
        "details": [
            ("What it was built to do",
             "Saturn V was NASA’s heavy-lift launch vehicle for the Apollo lunar program. "
             "It lifted Apollo spacecraft out of Earth’s gravity and sent them toward the Moon. "
             "It also launched the Skylab space station."),
            ("How its stages worked",
             "The first stage used five F-1 engines to lift the rocket from the pad. After its "
             "propellant was spent, it separated. The second stage continued accelerating the vehicle "
             "with five J-2 engines. The third stage helped place Apollo into Earth orbit, then "
             "restarted to send the spacecraft toward the Moon."),
            ("The spacecraft above the rocket",
             "Saturn V did not land on the Moon. It launched the Apollo command and service modules "
             "and lunar module. Two astronauts descended in the lunar module while the third stayed "
             "in orbit. The command module brought the crew home."),
            ("Why it matters",
             "Apollo 11 became the first crewed Moon landing in July 1969. Saturn V flew 13 times "
             "between 1967 and 1973. Its size and carefully sequenced stages made Apollo missions possible."),
        ],
        "source": "https://www.nasa.gov/mission/apollo-11/",
    },
    "Space Shuttle": {
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1500&q=90",
        "era": "UNITED STATES · 1981–2011",
        "short": "A reusable orbiter launched alongside two solid rocket boosters.",
        "facts": ["REUSABLE ORBITER", "135 MISSIONS"],
        "details": [
            ("A spacecraft and rocket together",
             "The Space Shuttle was a launch system built around a reusable, winged orbiter. At liftoff, "
             "the orbiter’s three main engines drew propellant from a large external tank, while two "
             "solid rocket boosters supplied additional thrust."),
            ("From launch to landing",
             "After reaching orbit, the orbiter operated as a spacecraft. It carried astronauts, satellites, "
             "laboratory equipment, and cargo. At the end of a mission it re-entered the atmosphere and "
             "glided to a runway landing."),
            ("What it accomplished",
             "Shuttle crews deployed and repaired satellites, carried the Hubble Space Telescope, supported "
             "science missions, and helped assemble the International Space Station."),
            ("A demanding design",
             "The boosters were recovered and the orbiter was refurbished for later flights, but the "
             "external tank was discarded. The program ended in 2011 after 135 missions."),
        ],
        "source": "https://www.nasa.gov/space-shuttle/",
    },
    "Soyuz": {
        "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1500&q=90",
        "era": "SOVIET UNION / RUSSIA · 1966–PRESENT",
        "short": "A long-running launch family used for crew, cargo, and satellite missions.",
        "facts": ["CREW & CARGO", "ISS ACCESS"],
        "details": [
            ("A family of launch vehicles",
             "Soyuz refers to a series of launch vehicles developed from the Soviet R-7 rocket lineage. "
             "Different versions have flown across decades, with upgrades to engines, guidance, and payload systems."),
            ("How the launcher is arranged",
             "The familiar configuration has a central core surrounded by four strap-on boosters. The side "
             "boosters ignite at liftoff and are discarded after their propellant is spent. The central stage "
             "continues the climb, followed by an upper stage that places the payload into orbit."),
            ("Human spaceflight and station service",
             "Soyuz spacecraft have carried crews to orbit and to space stations, including the International "
             "Space Station. Related launch vehicles have also sent cargo craft and satellites."),
            ("Why it became well known",
             "Its long service history and repeated upgrades made Soyuz one of the most familiar crew launch "
             "systems. Its role has changed as other countries and commercial providers developed crew vehicles."),
        ],
        "source": "https://www.nasa.gov/international-space-station/soyuz/",
    },
    "Falcon 9": {
        "image": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?auto=format&fit=crop&w=1500&q=90",
        "era": "UNITED STATES · 2010–PRESENT",
        "short": "A two-stage launcher for satellites and Dragon spacecraft.",
        "facts": ["PARTIALLY REUSABLE", "ORBITAL LAUNCH"],
        "details": [
            ("Built for orbit",
             "Falcon 9 is a two-stage rocket designed to carry satellites, cargo spacecraft, and crewed "
             "Dragon spacecraft to orbit. Its first stage provides the initial push through the lower "
             "atmosphere. The second stage finishes the climb and releases the payload."),
            ("The booster comes back",
             "After stage separation, the first stage can use engine burns and grid fins to guide itself "
             "toward a landing. Depending on the mission, it may land on a drone ship at sea or a landing "
             "pad. A recovered booster can be inspected and prepared for another flight."),
            ("Why reuse changed launch operations",
             "Recovering and reusing the first stage made repeat flights a central part of Falcon 9 operations. "
             "Reuse still requires inspections and refurbishment when needed."),
            ("What it launches",
             "Falcon 9 missions include communications and science satellites, rideshare payloads, and Dragon "
             "flights to the International Space Station."),
        ],
        "source": "https://www.spacex.com/vehicles/falcon-9/",
    },
    "Falcon Heavy": {
        "image": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1500&q=90",
        "era": "UNITED STATES · 2018–PRESENT",
        "short": "Three Falcon first-stage cores work together for heavy-lift missions.",
        "facts": ["THREE CORES", "HEAVY LIFT"],
        "details": [
            ("Three cores working together",
             "Falcon Heavy combines three Falcon first-stage cores: a central core and two side boosters. "
             "All three provide thrust at liftoff. After the side boosters separate, the center core "
             "continues firing before handing the vehicle to its upper stage."),
            ("A demanding payload class",
             "Heavy-lift missions can place large payloads into orbit or send spacecraft toward destinations "
             "that need more energy. Payload capacity depends on target orbit, trajectory, and recovery plan."),
            ("The first flight",
             "Falcon Heavy’s first test flight took place in February 2018. Its demonstration payload was "
             "a Tesla Roadster placed into an orbit around the Sun."),
            ("How it differs from Falcon 9",
             "Falcon 9 has one first-stage core. Falcon Heavy adds two side boosters around a reinforced "
             "center core, giving it a different lift capability."),
        ],
        "source": "https://www.spacex.com/vehicles/falcon-heavy/",
    },
    "Space Launch System": {
        "image": "https://images.unsplash.com/photo-1464802686167-b939a6910659?auto=format&fit=crop&w=1500&q=90",
        "era": "UNITED STATES · NASA ARTEMIS",
        "short": "NASA’s heavy-lift rocket for Orion and deep-space missions.",
        "facts": ["ARTEMIS", "DEEP SPACE"],
        "details": [
            ("Designed for missions beyond Earth orbit",
             "NASA’s Space Launch System, or SLS, is a heavy-lift rocket for the Artemis program. "
             "It launches Orion, the crew spacecraft, toward the Moon and other deep-space destinations."),
            ("Core stage and boosters",
             "The large core stage contains liquid propellant and four RS-25 engines. Two solid rocket "
             "boosters mounted beside it add thrust at liftoff. After they separate, the core stage "
             "continues the powered climb, and an upper stage helps send Orion on its trajectory."),
            ("Artemis I",
             "In November 2022, the first SLS launched Orion on Artemis I, an uncrewed test mission that "
             "traveled around the Moon and returned to Earth."),
            ("Rocket and spacecraft are a team",
             "SLS provides the launch energy; Orion carries the crew, life-support systems, and supplies. "
             "A lunar landing requires additional spacecraft and operations."),
        ],
        "source": "https://www.nasa.gov/humans-in-space/space-launch-system/",
    },
    "Starship": {
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1500&q=90",
        "era": "DEVELOPMENT PROGRAM · FLIGHT TESTS",
        "short": "A super-heavy launch system designed for eventual full reusability.",
        "facts": ["REUSABILITY GOAL", "IN DEVELOPMENT"],
        "details": [
            ("A two-part launch system",
             "Starship is the name of both the upper-stage spacecraft and the complete launch system. "
             "The full stack pairs the Super Heavy first-stage booster with the Starship vehicle above it."),
            ("Propellant and engines",
             "The system uses liquid methane and liquid oxygen. Super Heavy provides the initial thrust "
             "from Earth, while Starship’s engines are designed to operate in the upper atmosphere and in space."),
            ("What it is being developed for",
             "The development program aims at a reusable system for launching payloads and supporting future "
             "missions in space. NASA has selected a Starship-derived vehicle for a role in Artemis lunar "
             "landing plans, subject to development and mission requirements."),
            ("Testing and uncertainty",
             "Starship is a development program. Test flights help teams learn about launch, separation, "
             "flight, and recovery systems. Capabilities and schedules can change as the design evolves."),
        ],
        "source": "https://www.spacex.com/vehicles/starship/",
    },
}

MISSIONS = [
    ("1957", "Sputnik 1", "The first artificial satellite to orbit Earth.",
     "https://www.nasa.gov/image-article/sputnik-1/"),
    ("1961", "Vostok 1", "Yuri Gagarin became the first human to orbit Earth.",
     "https://science.nasa.gov/resource/yuri-gagarin-first-human-in-space/"),
    ("1969", "Apollo 11", "The first crewed Moon landing. Armstrong and Aldrin landed; Collins orbited above.",
     "https://www.nasa.gov/mission/apollo-11/"),
    ("1977", "Voyager 1 & 2", "Twin probes explored the outer planets and continued into interstellar space.",
     "https://science.nasa.gov/mission/voyager/"),
    ("1981", "STS-1 · Columbia", "The first Space Shuttle mission tested the reusable orbiter system.",
     "https://www.nasa.gov/mission/sts-1/"),
    ("1998", "International Space Station", "The first station module began an international orbital laboratory.",
     "https://www.nasa.gov/mission_pages/station/main/index.html"),
    ("2011", "Curiosity to Mars", "An Atlas V launched the rover to study Mars’s geology and past habitability.",
     "https://science.nasa.gov/mission/mars-science-laboratory/"),
    ("2020", "Perseverance & Ingenuity", "A rover and small helicopter reached Mars to study its ancient environment.",
     "https://science.nasa.gov/mission/mars-2020-perseverance/"),
    ("2021", "James Webb Space Telescope", "An Ariane 5 launched Webb on its journey to its observing orbit.",
     "https://science.nasa.gov/mission/james-webb-space-telescope/"),
    ("2022", "Artemis I", "SLS launched Orion on an uncrewed test flight around the Moon and back.",
     "https://www.nasa.gov/mission/artemis-i/"),
    ("2023", "Chandrayaan-3", "India’s LVM3 launched the lunar mission that achieved a soft landing.",
     "https://www.isro.gov.in/Chandrayaan3.html"),
]

ANSWERS = [
    (r"who.*(step|walk|land).*(moon)|who.*first.*moon|first.*(person|human|astronaut).*moon",
     "Neil Armstrong was the first person to step onto the Moon. Buzz Aldrin followed him. "
     "Their Apollo 11 crewmate Michael Collins stayed in lunar orbit. Apollo 11 landed in July 1969."),
    (r"who.*(second|next).*(moon)|second.*(person|human).*moon",
     "Buzz Aldrin was the second person to walk on the Moon, following Neil Armstrong during Apollo 11."),
    (r"first human.*space|first astronaut.*space|gagarin|vostok",
     "Yuri Gagarin was the first human in space. In 1961, he orbited Earth once aboard Vostok 1."),
    (r"first woman.*space|woman.*space|tereshkova",
     "Valentina Tereshkova became the first woman in space in June 1963, aboard Vostok 6."),
    (r"first american.*orbit|john glenn|friendship 7",
     "John Glenn became the first American to orbit Earth in 1962 aboard Friendship 7."),
    (r"first american.*space|alan shepard|freedom 7",
     "Alan Shepard was the first American in space. His 1961 flight was suborbital. "
     "John Glenn later became the first American to orbit Earth."),
    (r"sputnik",
     "Sputnik 1 was the first artificial satellite to orbit Earth. The Soviet Union launched it in 1957."),
    (r"apollo\s*11|moon landing|first moon landing",
     "Apollo 11 was the first mission to land people on the Moon. Neil Armstrong and Buzz Aldrin "
     "landed in the Eagle lunar module while Michael Collins orbited above."),
    (r"apollo\s*13",
     "Apollo 13 launched toward the Moon in 1970, but an oxygen tank failure damaged the spacecraft. "
     "Jim Lovell, Jack Swigert, and Fred Haise returned safely; the mission did not land."),
    (r"stage|staging",
     "Rocket staging means dropping an empty stage after its engines and fuel have done their job. "
     "The next stage then pushes a lighter vehicle onward."),
    (r"artemis|sls|space launch system",
     "Artemis I was the uncrewed 2022 test flight of NASA’s SLS rocket and Orion spacecraft around the Moon and back."),
    (r"falcon\s*heavy",
     "Falcon Heavy combines three Falcon first-stage cores: two side boosters and a center core."),
    (r"falcon\s*9|reus|booster landing",
     "Falcon 9 is a two-stage rocket. Its first stage can return to a landing pad or drone ship for recovery and possible reuse."),
    (r"soyuz",
     "Soyuz is both a Russian launch-vehicle family and the name of a crew spacecraft. Soyuz launchers have carried astronauts, cargo, and satellites."),
    (r"space shuttle|shuttle",
     "NASA’s Space Shuttle was a reusable winged orbiter launched with two solid rocket boosters and a large external tank. It flew 135 missions."),
    (r"starship",
     "Starship is SpaceX’s developing launch system: a Super Heavy booster beneath a Starship upper vehicle. It is designed for eventual full reusability."),
    (r"voyager",
     "Voyager 1 and 2 launched in 1977 to study the outer planets. Both spacecraft later traveled into interstellar space."),
    (r"curiosity",
     "Curiosity is NASA’s Mars rover. It landed in Gale Crater in 2012 after launching on an Atlas V."),
    (r"perseverance|ingenuity",
     "Perseverance landed on Mars in 2021. It carried Ingenuity, the helicopter that demonstrated powered flight on Mars."),
    (r"chandrayaan",
     "Chandrayaan-3 was India’s lunar mission, launched by LVM3 in 2023. Its lander achieved a soft landing."),
    (r"james webb|\bwebb\b|jwst",
     "The James Webb Space Telescope launched on an Ariane 5 in 2021 and observes mainly in infrared light."),
    (r"hubble",
     "The Hubble Space Telescope launched aboard Space Shuttle Discovery in 1990."),
    (r"international space station|\biss\b|space station",
     "The International Space Station is a research laboratory in low Earth orbit. Its first module launched in 1998."),
    (r"mars|red planet",
     "Mars exploration uses orbiters, landers, and rovers. Curiosity and Perseverance study its rocks and ancient environments."),
    (r"rocket|thrust|how.*(fly|work)|space",
     "A rocket moves forward by pushing exhaust backward. It carries fuel and oxidizer, so its engines can work in the vacuum of space."),
]


def answer_guide(question: str) -> str:
    for pattern, answer in ANSWERS:
        if re.search(pattern, question, re.IGNORECASE):
            return answer
    return (
        "I don’t have that detail in my offline guide yet. Try asking about Apollo 11, "
        "who first walked on the Moon, Sputnik, Vostok 1, Mars rovers, Voyager, or one of the rockets."
    )


# -------------------------------- CSS --------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --ink:#f4f6fb; --muted:#a0aaba; --bg:#070b14;
  --cyan:#7be4f3; --line:rgba(211,225,255,.13);
}
html { scroll-behavior:smooth; }
.stApp {
  background:
    radial-gradient(ellipse at 12% 2%,rgba(36,73,110,.16),transparent 36%),
    #070b14;
  color:var(--ink);
  font-family:Manrope,sans-serif;
}
header[data-testid="stHeader"] { background:rgba(7,11,20,.8); }
.block-container { max-width:1280px; padding:1rem 2rem 4rem; }
h1,h2,h3 { letter-spacing:-.06em; }
h1 { font-size:clamp(3.7rem,8vw,7rem)!important; line-height:.94!important; }
h2 { font-size:clamp(2.5rem,5vw,4.3rem)!important; line-height:1!important; }
p { color:#c4cdda; }
.eyebrow,.tag {
  color:var(--cyan); font:10px 'DM Mono',monospace;
  letter-spacing:.13em; text-transform:uppercase;
}

.site-nav {
  position:fixed; z-index:999; top:0; left:0; width:100%; height:74px;
  background:rgba(7,11,20,.92); backdrop-filter:blur(18px);
  border-bottom:1px solid var(--line);
}
.site-nav-inner {
  max-width:1200px; height:100%; margin:auto; padding:0 24px;
  display:flex; justify-content:space-between; align-items:center;
}
.site-logo {
  color:white; font-size:12px; font-weight:800; letter-spacing:.06em;
  text-decoration:none!important;
}
.logo-star {
  display:inline-grid; place-items:center; width:30px; height:30px;
  margin-right:10px; color:var(--cyan); border:1px solid var(--cyan);
  border-radius:50%; font-size:15px;
}
.site-links { display:flex; align-items:center; gap:28px; }
.site-links a {
  color:#c5ccda!important; text-decoration:none!important;
  font:10px 'DM Mono',monospace; letter-spacing:.12em;
}
.site-links a:hover { color:var(--cyan)!important; }
.site-links .contact-link { border:1px solid rgba(123,228,243,.45); padding:11px 14px; }

.hero {
  height:calc(100vh - 74px); min-height:640px; max-height:960px;
  width:100vw; margin-top:74px; margin-left:calc(50% - 50vw);
  padding:0 max(24px,calc((100vw - 1200px)/2));
  position:relative; display:flex; flex-direction:column; justify-content:flex-end;
  overflow:hidden;
  background:
    linear-gradient(90deg,rgba(4,8,15,.88),rgba(4,8,15,.30)),
    linear-gradient(0deg,#070b14,transparent 48%),
    url('https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&w=2200&q=90')
      center 43%/cover;
}
.hero:before {
  content:""; position:absolute; inset:0; pointer-events:none; opacity:.55;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);
  background-size:88px 88px;
}
.hero-content { position:relative; max-width:760px; padding-bottom:100px; animation:riseIn .8s ease-out both; }
.hero h1 { margin:28px 0 24px; }
.hero p { max-width:520px; font-size:19px; line-height:1.6; }
.hero-actions { display:flex; align-items:center; gap:24px; margin-top:30px; }
.hero-button {
  display:inline-block; padding:15px 19px; background:var(--cyan);
  color:#000!important; text-decoration:none!important; font-size:12px;
  font-weight:800; transition:transform .25s,background .25s;
}
.hero-button:hover { transform:translateY(-3px); background:#a4f3ff; }
.hero-secondary { color:#d5dbe5!important; text-decoration:none!important; font-size:12px; }
.hero-bottom { position:absolute; bottom:28px; color:#aab3c1; font:9px 'DM Mono',monospace; }
.hero-bottom.left { left:max(24px,calc((100vw - 1200px)/2)); }
.hero-bottom.right { right:max(24px,calc((100vw - 1200px)/2)); }

.section-head {
  display:grid; grid-template-columns:1fr 1fr; gap:35px;
  align-items:end; margin:106px 0 48px; animation:riseIn .7s ease-out both;
}
.section-head h2 { margin:17px 0 0; }
.section-head p { max-width:450px; margin:0 0 4px; font-size:14px; }

.rocket-grid { display:grid; grid-template-columns:repeat(12,1fr); gap:17px; }
.rocket-card {
  position:relative; isolation:isolate; overflow:hidden; min-height:390px;
  padding:25px; display:flex; flex-direction:column; justify-content:flex-end;
  color:white; background-size:cover; background-position:center;
  border:1px solid var(--line);
  transition:transform .35s ease,box-shadow .35s ease;
  animation:riseIn .65s ease-out both;
}
.rocket-card:nth-child(1),.rocket-card:nth-child(4),.rocket-card:nth-child(6) { grid-column:span 7; }
.rocket-card:nth-child(2),.rocket-card:nth-child(3),.rocket-card:nth-child(5),.rocket-card:nth-child(7) { grid-column:span 5; }
.rocket-card:nth-child(2) { animation-delay:.08s; }
.rocket-card:nth-child(3) { animation-delay:.16s; }
.rocket-card:nth-child(4) { animation-delay:.24s; }
.rocket-card:nth-child(5) { animation-delay:.32s; }
.rocket-card:nth-child(6) { animation-delay:.40s; }
.rocket-card:nth-child(7) { animation-delay:.48s; }
.rocket-card h3 { color:white; font-size:29px; margin:10px 0 7px; }
.rocket-card p { color:#c1cad7; font-size:12px; line-height:1.6; margin:0; }
.rocket-meta { display:flex; gap:13px; margin-top:17px; color:#a9b6c6; font:9px 'DM Mono',monospace; }

.profile-tab {
  margin:25px 0 45px;
  background:linear-gradient(135deg,#101927,#080d16 70%);
  border:1px solid rgba(123,228,243,.28);
  animation:riseIn .45s ease-out both;
}
.profile-tab-bar {
  min-height:60px; padding:12px 20px;
  display:flex; align-items:center;
  background:rgba(8,13,22,.96);
  border-bottom:1px solid var(--line);
  color:var(--cyan);
  font:10px 'DM Mono',monospace; letter-spacing:.12em;
}
.profile-hero {
  min-height:330px; padding:30px;
  display:flex; flex-direction:column; justify-content:flex-end;
  background-size:cover; background-position:center;
}
.profile-hero h2 { color:white; margin:12px 0 8px; }
.profile-hero p { max-width:650px; margin:0; }
.profile-body { padding:28px; }
.profile-body h3 { color:var(--cyan); margin:28px 0 8px; }
.profile-body p { max-width:820px; line-height:1.8; }
.profile-source {
  display:inline-block; margin-top:24px; padding:12px 15px;
  border:1px solid rgba(123,228,243,.4); color:var(--cyan)!important;
  text-decoration:none!important; font:9px 'DM Mono',monospace; letter-spacing:.08em;
}
.fact {
  display:inline-block; padding:8px 11px; margin:7px 7px 7px 0;
  border:1px solid var(--line); color:#c4cdda;
  font:9px 'DM Mono',monospace; letter-spacing:.08em;
}

.mission-list { border-top:1px solid var(--line); }
.mission {
  display:grid; grid-template-columns:95px 1fr 1.15fr 30px; gap:22px;
  align-items:center; padding:23px 5px; border-bottom:1px solid var(--line);
  color:inherit!important; text-decoration:none!important;
  transition:padding .25s ease,background .25s ease;
  animation:riseIn .5s ease-out both;
}
.mission:hover { padding-left:16px; background:rgba(123,228,243,.04); }
.mission-year { color:var(--cyan); font:12px 'DM Mono',monospace; }
.mission h3 { margin:0; font-size:18px; }
.mission p { margin:0; font-size:12px; }
.mission-arrow { color:var(--cyan); }

.comparison { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.compare-card {
  padding:21px; background:#0d1420; border:1px solid var(--line);
  transition:transform .25s,border-color .25s;
}
.compare-card:hover { transform:translateY(-4px); border-color:rgba(123,228,243,.4); }
.compare-card h3 { margin:9px 0; font-size:17px; }
.compare-card p { min-height:58px; margin:0; font-size:11px; }
.bar { height:2px; background:#202d3c; margin-top:20px; }
.bar span { display:block; height:100%; background:var(--cyan); }

.lab,.ai-section {
  margin-top:100px; padding:64px 0;
  background:linear-gradient(140deg,#101927,#080d16 70%);
  border-block:1px solid rgba(255,255,255,.05);
}
.readout-visual {
  min-height:420px; padding:28px;
  display:flex; flex-direction:column; justify-content:space-between;
  background-size:cover; background-position:center;
  border:1px solid rgba(123,228,243,.25);
  animation:riseIn .6s ease-out both;
}
.readout-number { color:var(--cyan); font-size:clamp(54px,7vw,82px); line-height:1; letter-spacing:-.07em; margin-top:24px; }
.readout-meter { height:5px; background:rgba(255,255,255,.2); margin:18px 0 10px; }
.readout-meter span { display:block; height:100%; background:var(--cyan); transition:width .7s ease; }
.readout-label { color:var(--cyan); font:9px 'DM Mono',monospace; letter-spacing:.12em; }
.readout-copy { max-width:390px; font-size:13px; }
.readout-stats { display:grid; grid-template-columns:1fr 1fr; gap:14px; padding-top:16px; border-top:1px solid rgba(211,225,255,.2); }
.readout-stats span { color:var(--muted); font:9px 'DM Mono',monospace; }
.readout-stats b { display:block; color:var(--ink); font:13px Manrope,sans-serif; margin-top:5px; }

.ai-grid { display:grid; grid-template-columns:.72fr 1.28fr; gap:38px; }
.ai-copy { color:var(--muted); font-size:14px; }
.local-badge {
  display:inline-block; padding:9px 11px; margin-top:12px;
  border:1px solid rgba(123,228,243,.3); color:var(--cyan);
  font:9px 'DM Mono',monospace; letter-spacing:.1em;
}
.footer {
  margin-top:80px; padding:22px 0; border-top:1px solid var(--line);
  color:#758093; font:9px 'DM Mono',monospace; letter-spacing:.1em;
}
.footer-inner { display:flex; justify-content:space-between; gap:16px; }

div.stButton > button, div.stFormSubmitButton > button {
  border:1px solid rgba(123,228,243,.4);
  border-radius:2px;
  background:var(--cyan);
  color:#000000 !important;
  font-weight:800;
}
div.stButton > button *, div.stFormSubmitButton > button * {
  color:#000000 !important;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
  background:#a4f3ff;
  color:#000000 !important;
}
[data-testid="stChatMessage"] { background:#101725; border:1px solid var(--line); }

@keyframes riseIn {
  from { opacity:0; transform:translateY(24px); }
  to { opacity:1; transform:translateY(0); }
}
@media(max-width:760px) {
  .block-container { padding:1rem 1rem 3rem; }
  .site-links { gap:12px; }
  .site-links a { font-size:8px; }
  .site-links .contact-link { display:none; }
  .hero { min-height:620px; padding-left:22px; padding-right:22px; }
  .hero p { font-size:16px; }
  .hero-actions { align-items:flex-start; flex-direction:column; gap:15px; }
  .hero-bottom.right { display:none; }
  .section-head { display:block; margin:78px 0 34px; }
  .section-head p { margin-top:18px; }
  .rocket-card,.rocket-card:nth-child(n) { grid-column:span 12; min-height:350px; }
  .profile-hero { min-height:270px; padding:22px; }
  .profile-body { padding:20px; }
  .mission { grid-template-columns:65px 1fr 22px; gap:12px; }
  .mission p { grid-column:2; }
  .comparison { grid-template-columns:1fr 1fr; }
  .footer-inner { flex-direction:column; }
}
@media(max-width:430px) {
  .site-logo { font-size:9px; }
  .site-links { gap:8px; }
  .site-links a { font-size:7px; letter-spacing:.07em; }
  .comparison { grid-template-columns:1fr; }
  .hero h1 { font-size:52px!important; }
}
@media(prefers-reduced-motion:reduce) {
  *,*:before,*:after {
    scroll-behavior:auto!important;
    transition-duration:.01ms!important;
    animation-duration:.01ms!important;
  }
}
</style>
""", unsafe_allow_html=True)


# ------------------------------ NAV + HERO ------------------------------

st.markdown("""
<header class="site-nav">
  <div class="site-nav-inner">
    <a class="site-logo" href="#top"><span class="logo-star">✦</span> BEYOND EARTH</a>
    <nav class="site-links">
      <a href="#rockets">ROCKETS</a>
      <a href="#missions">MISSIONS</a>
      <a href="#launch-lab">LAUNCH LAB</a>
      <a href="#local-guide">AI GUIDE</a>
      <a class="contact-link" href="#contact">GET IN TOUCH ↗</a>
    </nav>
  </div>
</header>
<div id="top"></div>
<section class="hero">
  <div class="hero-content">
    <div class="eyebrow">A FIELD GUIDE TO SPACEFLIGHT　/　01—04</div>
    <h1>We built a way<br>to leave Earth.</h1>
    <p>Meet the machines that carried explorers to the Moon, opened space to science,
    and are shaping what comes next.</p>
    <div class="hero-actions">
      <a class="hero-button" href="#rockets">EXPLORE THE ROCKETS　↘</a>
      <a class="hero-secondary" href="#missions">Jump to missions　↓</a>
    </div>
  </div>
  <div class="hero-bottom left">SCROLL TO EXPLORE</div>
  <div class="hero-bottom right">A VISUAL GUIDE TO LAUNCH VEHICLES & MISSIONS</div>
</section>
""", unsafe_allow_html=True)


# -------------------------------- BASICS ----------------------------------

st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">01 / THE BASICS</div>
    <h2>A rocket is a<br>controlled escape.</h2>
  </div>
  <p>It pushes hot gas down, and that reaction drives the vehicle up.
  Every kilogram matters. Rockets shed empty stages as they climb, saving
  the remaining fuel for the journey ahead.</p>
</div>
<div class="comparison">
  <div class="compare-card"><div class="eyebrow">01 — THRUST</div>
    <h3>Push against nothing</h3>
    <p>Exhaust shot backward creates forward motion—even in a vacuum.</p></div>
  <div class="compare-card"><div class="eyebrow">02 — STAGING</div>
    <h3>Drop the dead weight</h3>
    <p>Spent stages separate so the next engines can keep accelerating.</p></div>
  <div class="compare-card"><div class="eyebrow">03 — PAYLOAD</div>
    <h3>The reason for the ride</h3>
    <p>People, satellites, probes, and supplies travel above the rocket.</p></div>
</div>
""", unsafe_allow_html=True)


# ----------------------------- ROCKET LIBRARY -----------------------------

st.markdown('<div id="rockets"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">02 / THE VEHICLES</div>
    <h2>Different rockets.<br>One big ambition.</h2>
  </div>
  <p>From the Moon race to reusable boosters, every vehicle reflects the missions
  and engineering ideas of its time.</p>
</div>
""", unsafe_allow_html=True)

if "active_rocket" not in st.session_state:
    st.session_state.active_rocket = None

if st.session_state.active_rocket:
    name = st.session_state.active_rocket
    rocket = ROCKETS[name]

    tab_title_col, close_col = st.columns([5, 1])
    with tab_title_col:
        st.markdown(
            '<div class="profile-tab-bar">ROCKET PROFILE / FULL EXPLANATION</div>',
            unsafe_allow_html=True,
        )
    with close_col:
        if st.button("CLOSE TAB ×", key="close_rocket_tab"):
            st.session_state.active_rocket = None
            st.rerun()

    facts_html = "".join(
        f'<span class="fact">{escape(fact)}</span>'
        for fact in rocket["facts"]
    )
    details_html = "".join(
        f'<h3>{escape(heading)}</h3><p>{escape(paragraph)}</p>'
        for heading, paragraph in rocket["details"]
    )

    profile_html = f"""
    <div class="profile-tab">
      <div class="profile-hero" style="
        background-image:
          linear-gradient(0deg,rgba(4,8,14,.97),rgba(4,8,14,.12)),
          url('{rocket["image"]}');
      ">
        <div class="eyebrow">{escape(rocket["era"])}</div>
        <h2>{escape(name)}</h2>
        <p>{escape(rocket["short"])}</p>
      </div>
      <div class="profile-body">
        {facts_html}
        {details_html}
        <a class="profile-source" href="{escape(rocket["source"])}"
           target="_blank" rel="noreferrer">
          READ MORE FROM THE OFFICIAL SOURCE ↗
        </a>
      </div>
    </div>
    """
    st.markdown(profile_html, unsafe_allow_html=True)

else:
    rocket_names = list(ROCKETS.keys())

    for start in range(0, len(rocket_names), 2):
        row_names = rocket_names[start:start + 2]

        if len(row_names) == 1:
            columns = st.columns([12])
        elif start % 4 == 0:
            columns = st.columns([7, 5], gap="medium")
        else:
            columns = st.columns([5, 7], gap="medium")

        for column, name in zip(columns, row_names):
            rocket = ROCKETS[name]

            with column:
                card_html = f"""
                <div class="rocket-card" style="
                  background-image:
                    linear-gradient(0deg,rgba(4,8,14,.97),rgba(4,8,14,.04) 78%),
                    url('{rocket["image"]}');
                ">
                  <div class="tag">{escape(rocket["era"])}</div>
                  <h3>{escape(name)}</h3>
                  <p>{escape(rocket["short"])}</p>
                  <div class="rocket-meta">
                    {escape(rocket["facts"][0])}　·　{escape(rocket["facts"][1])}
                  </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button("OPEN FULL EXPLANATION ↗", key=f"open_{name}"):
                    st.session_state.active_rocket = name
                    st.rerun()

# Stop rendering the rest of the page while a rocket profile is open.
# The close button clears active_rocket and reruns, so the page returns below.
if st.session_state.active_rocket:
    st.stop()


# -------------------------------- MISSIONS ---------------------------------

st.markdown('<div id="missions"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">03 / LANDMARK MISSIONS</div>
    <h2>Milestones on<br>the way out.</h2>
  </div>
  <p>Each mission needed the right rocket, the right moment, and teams that could
  turn ambitious physics into a safe journey.</p>
</div>
""", unsafe_allow_html=True)

mission_html = ['<div class="mission-list">']
for year, name, description, url in MISSIONS:
    mission_html.append(
        f'<a class="mission" href="{url}" target="_blank" rel="noreferrer">'
        f'<span class="mission-year">{escape(year)}</span>'
        f'<h3>{escape(name)}</h3>'
        f'<p>{escape(description)}</p>'
        f'<span class="mission-arrow">↗</span></a>'
    )
mission_html.append("</div>")
st.markdown("".join(mission_html), unsafe_allow_html=True)


# ----------------------------- COMPARISON ---------------------------------

st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">04 / CHOOSE YOUR RIDE</div>
    <h2>Match the rocket<br>to the mission.</h2>
  </div>
  <p>Bars show broad mission roles only; they are illustrative, not to scale.</p>
</div>
""", unsafe_allow_html=True)

comparison = [
    ("Soyuz", "CREW + CARGO", 45, "Crew transport and cargo flights to low Earth orbit."),
    ("Falcon 9", "REUSABLE ORBIT", 58, "Satellite launches and Dragon missions to orbit."),
    ("Falcon Heavy", "HEAVY LIFT", 78, "Large payloads and demanding orbital missions."),
    ("SLS", "LUNAR EXPLORATION", 88, "Orion and Artemis missions beyond Earth orbit."),
]
comparison_html = ['<div class="comparison">']
for name, role, value, description in comparison:
    comparison_html.append(
        f'<div class="compare-card"><div class="eyebrow">{escape(role)}</div>'
        f'<h3>{escape(name)}</h3><p>{escape(description)}</p>'
        f'<div class="bar"><span style="width:{value}%"></span></div></div>'
    )
comparison_html.append("</div>")
st.markdown("".join(comparison_html), unsafe_allow_html=True)


# ------------------------------- LAUNCH LAB -------------------------------

st.markdown('<div id="launch-lab"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">05 / INTERACTIVE LAUNCH LAB</div>
    <h2>Build a mission.<br>Check the basics.</h2>
  </div>
  <p>Adjust payload, fuel, and destination, then run a simplified readiness estimate.
  This is an educational toy model, not a real launch calculation.</p>
</div>
""", unsafe_allow_html=True)

lab_left, lab_right = st.columns([1, 1], gap="large")

with lab_left:
    destination = st.selectbox(
        "Destination",
        ["Low Earth orbit", "The Moon", "Mars transfer"],
    )
    payload = st.slider("Payload mass (tonnes)", 1, 60, 12)
    fuel = st.slider("Fuel reserve (%)", 10, 100, 72)
    vehicle = st.selectbox(
        "Launch vehicle",
        ["Falcon 9", "Falcon Heavy", "SLS", "Starship"],
    )
    run_check = st.button("RUN READINESS CHECK ↗", key="run_check")

if "readiness" not in st.session_state:
    st.session_state.readiness = None

if run_check:
    capacities = {"Falcon 9": 24, "Falcon Heavy": 64, "SLS": 95, "Starship": 100}
    destination_factor = {
        "Low Earth orbit": 1.0,
        "The Moon": 0.78,
        "Mars transfer": 0.62,
    }
    estimate = round(
        (100 - payload / capacities[vehicle] * 58)
        * (0.55 + fuel / 220)
        * destination_factor[destination]
    )
    st.session_state.readiness = max(8, min(98, estimate))

with lab_right:
    score = st.session_state.readiness

    if score is None:
        score_text = "—"
        meter_width = 0
        state_text = "AWAITING CONFIGURATION"
        copy_text = "Set your mission parameters and run a check to see the result."
    elif score > 68:
        score_text = f"{score}%"
        meter_width = score
        state_text = "READINESS LOOKS PROMISING"
        copy_text = (
            "This simplified model sees a workable combination. "
            "Real mission design needs detailed engineering and safety reviews."
        )
    else:
        score_text = f"{score}%"
        meter_width = score
        state_text = "REVIEW YOUR CONFIGURATION"
        copy_text = (
            "Try adjusting the payload, fuel reserve, vehicle, or destination. "
            "This is an educational estimate, not a real launch prediction."
        )

    rocket_image = (
        "https://images.unsplash.com/photo-1517976487492-5750f3195933"
        "?auto=format&fit=crop&w=1400&q=90"
    )
    readout_html = f"""
    <div class="readout-visual" style="
      background-image:
        linear-gradient(0deg,rgba(4,8,14,.97),rgba(4,8,14,.38)),
        url('{rocket_image}');
    ">
      <div>
        <div class="eyebrow">MISSION READINESS</div>
        <div class="readout-number">{score_text}</div>
        <div class="readout-meter"><span style="width:{meter_width}%"></span></div>
        <div class="readout-label">{state_text}</div>
        <p class="readout-copy">{escape(copy_text)}</p>
      </div>
      <div class="readout-stats">
        <span>DESTINATION<b>{escape(destination)}</b></span>
        <span>PAYLOAD<b>{payload} tonnes</b></span>
        <span>VEHICLE<b>{escape(vehicle)}</b></span>
        <span>MODEL TYPE<b>SIMPLIFIED</b></span>
      </div>
    </div>
    """
    st.markdown(readout_html, unsafe_allow_html=True)


# ------------------------------ LOCAL GUIDE -------------------------------

st.markdown('<div id="local-guide"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="ai-section">
  <div class="ai-grid">
    <div class="ai-copy">
      <div class="eyebrow">06 / ASK THE FLIGHT DESK</div>
      <h2>Your local<br>rocket guide.</h2>
      <p>Ask about rockets, astronauts, missions, or space milestones.
      This guide uses built-in answers and does not connect to an online AI service.</p>
      <span class="local-badge">LOCAL KNOWLEDGE MODE · NO API</span>
    </div>
    <div>
      <div class="eyebrow">MISSION CONTROL / ROCKET GUIDE</div>
      <p>Try asking: “Who stepped on the Moon first?” or “How does rocket staging work?”</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("assistant", "Welcome aboard. Ask me about rockets, missions, or space milestones.")
    ]

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

with st.form("local_guide_form", clear_on_submit=True):
    guide_question = st.text_input(
        "Ask Mission Control",
        placeholder="Who stepped on the Moon first?",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("SEND ↗")

if submitted and guide_question.strip():
    st.session_state.chat_history.append(("user", guide_question))
    st.session_state.chat_history.append(("assistant", answer_guide(guide_question)))
    st.rerun()


# -------------------------------- CONTACT ----------------------------------

st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-head">
  <div>
    <div class="eyebrow">GET IN TOUCH</div>
    <h2>Where will rockets<br>take us next?</h2>
  </div>
  <p>Have a question, favorite mission, or idea for this guide? Send a message.</p>
</div>
""", unsafe_allow_html=True)

with st.form("contact_form", clear_on_submit=True):
    contact_col1, contact_col2 = st.columns(2)

    with contact_col1:
        contact_name = st.text_input("Your name")

    with contact_col2:
        contact_email = st.text_input("Email address")

    contact_message = st.text_area("Your message", height=130)
    contact_submit = st.form_submit_button("SEND A MESSAGE ↗")

if contact_submit:
    if contact_name and contact_email and contact_message:
        st.success("Thanks! This demo form is ready to connect to an email service.")
    else:
        st.warning("Please fill in your name, email, and message.")

st.markdown("""
<div class="footer">
  <div class="footer-inner">
    <span>BEYOND EARTH · ROCKETS & MISSIONS</span>
    <span>IMAGES VIA UNSPLASH · MISSION LINKS VIA NASA / ISRO</span>
    <a href="#top">BACK TO TOP ↑</a>
  </div>
</div>
""", unsafe_allow_html=True)
