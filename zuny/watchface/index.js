import { MID } from './mid.js'

const N = hmUI.show_level.ONLY_NORMAL
const AOD = hmUI.show_level.ONLY_AOD
const seq = (p, n) => Array.from({ length: n || 10 }, (_, i) => `${p}_${i}.png`)
const ACC = ['mag', 'ora', 'cya', 'lim', 'pur']
const ACC_TITLES = ['magenta', 'orange', 'cyan', 'lime', 'purple']

// Native page urls (verified on Active 2 NFC Square, except heart/spo)
const APPS = {
  weather: 'WeatherScreen', steps: 'activityAppScreen', music: 'MusicCommonScreen',
  timer: 'CountdownAppScreen', calendar: 'ScheduleCalScreen', alarm: 'AlarmInfoScreen',
  heart: 'heart_app_Screen', spo: 'spo_HomeScreen', stress: 'StressHomeScreen', pai: 'PAI_app_Screen',
  alti: 'BaroAltimeterScreen', battery: 'Settings_batteryManagerScreen',
}
function launch(name) {
  try { hmApp.startApp({ url: APPS[name], native: true }) } catch (e) { console.log('launch fail ' + name + ' ' + e) }
}
function zone(x, y, w, h, fn) {
  const z = hmUI.createWidget(hmUI.widget.IMG, { x, y, w, h, src: 'hit.png', show_level: N })
  z.addEventListener(hmUI.event.CLICK_UP, fn)
  return z
}
function getInt(k, d) { try { const v = hmFS.SysProGetInt(k); return v === undefined || v === null ? d : v } catch (e) { return d } }
function setInt(k, v) { try { hmFS.SysProSetInt(k, v) } catch (e) {} }

function opt(type, title, preview) {
  return { type, title_en: title, title_sc: title, title_tc: title, preview }
}
function editGroup(id, x, y, w, h, key, options, def, tipsX, tipsY) {
  const g = hmUI.createWidget(hmUI.widget.WATCHFACE_EDIT_GROUP, {
    edit_id: id, x, y, w, h,
    select_image: `ed_${key}_sel.png`, un_select_image: `ed_${key}_uns.png`,
    default_type: options[def].type, optional_types: options, count: options.length,
    tips_BG: 'ed_tip.png', tips_x: tipsX, tips_y: tipsY, tips_width: 130, tips_margin: 6,
  })
  const t = g.getProperty(hmUI.prop.CURRENT_TYPE)
  const i = options.findIndex((o) => o.type === t)
  return i < 0 ? def : i
}

WatchFace({
  build() {
    hmUI.createWidget(hmUI.widget.IMG, { x: 0, y: 0, src: 'bg.png', show_level: N | AOD })

    // ---------- edit groups ----------
    const accEd = editGroup(130, 4, 12, 200, 138, 'acc',
      ACC.map((k, i) => opt(100301 + i, ACC_TITLES[i], `ed_acc_${k}.png`)), 0, 36, 140)
    const mid = MID[editGroup(120, 208, 147, 178, 128, 'mid',
      MID.map((o) => opt(o.type, o.title, `ed_mid_${o.key}.png`)), 0, 24, -40)]
    const BOT = ['steps', 'cal']
    const bot = BOT[editGroup(121, 8, 380, 376, 66, 'bot', [
      opt(100211, 'steps', 'ed_bot_steps.png'), opt(100212, 'calories', 'ed_bot_cal.png'),
    ], 0, 120, -40)]

    // accent: editor choice wins when it changed; otherwise last tapped colour
    let accent = getInt('zuny_accent', accEd)
    if (getInt('zuny_acc_ed', -1) !== accEd) { accent = accEd; setInt('zuny_acc_ed', accEd); setInt('zuny_accent', accent) }

    // ---------- time ----------
    const hours = ACC.map((k, i) => {
      const w = hmUI.createWidget(hmUI.widget.IMG_TIME, {
        hour_zero: 1, hour_startX: 6, hour_startY: 16, hour_array: seq(`h_${k}`), hour_space: 0, show_level: N,
      })
      w.setProperty(hmUI.prop.VISIBLE, i === accent)
      return w
    })
    hmUI.createWidget(hmUI.widget.IMG_TIME, {
      minute_zero: 1, minute_startX: 6, minute_startY: 160, minute_array: seq('m'), minute_space: 0,
      minute_follow: 0, show_level: N,
    })
    hmUI.createWidget(hmUI.widget.IMG_TIME, {
      hour_zero: 1, hour_startX: 6, hour_startY: 16, hour_array: seq('a'), hour_space: 0,
      minute_zero: 1, minute_startX: 6, minute_startY: 160, minute_array: seq('a'), minute_space: 0,
      minute_follow: 0, show_level: AOD,
    })

    // ---------- date / battery / alarm ----------
    const WK = seq('wk', 7), MO = seq('mo', 12), G = seq('g')
    hmUI.createWidget(hmUI.widget.TEXT_IMG, {
      x: 212, y: 4, w: 170, h: 36, font_array: G, h_space: 0, align_h: hmUI.align.LEFT,
      type: hmUI.data_type.BATTERY, unit_en: 'g_pct.png', unit_sc: 'g_pct.png', unit_tc: 'g_pct.png', show_level: N,
    })
    hmUI.createWidget(hmUI.widget.IMG_WEEK, { x: 212, y: 34, week_en: WK, week_sc: WK, week_tc: WK, show_level: N | AOD })
    hmUI.createWidget(hmUI.widget.IMG_DATE, {
      month_startX: 212, month_startY: 76, month_is_character: true,
      month_en_array: MO, month_sc_array: MO, month_tc_array: MO,
      day_follow: 1, day_zero: 0, day_space: 0,
      day_en_array: G, day_sc_array: G, day_tc_array: G,
      show_level: N | AOD,
    })
    hmUI.createWidget(hmUI.widget.IMG_STATUS, { x: 211, y: 116, src: 'bell.png', type: hmUI.system_status.CLOCK, show_level: N })
    hmUI.createWidget(hmUI.widget.TEXT_IMG, {
      x: 238, y: 110, w: 100, h: 36, font_array: seq('w'), h_space: 0, dot_image: 'w_col.png',
      type: hmUI.data_type.ALARM_CLOCK, padding: true, invalid_image: 'hit.png', show_level: N,
    })

    // ---------- editable slot (cyan) ----------
    const C = seq('c')
    const u = (src) => (src ? { unit_en: src, unit_sc: src, unit_tc: src } : {})
    const num = (props) => hmUI.createWidget(hmUI.widget.TEXT_IMG, Object.assign({
      x: 212, y: 190, w: 174, h: 77, font_array: C, h_space: 0, invalid_image: 'c_none.png', show_level: N,
    }, props))
    if (mid.key === 'weather') {
      hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
        x: 212, y: 147, image_array: seq('wc', 29), image_length: 29, type: hmUI.data_type.WEATHER_CURRENT, show_level: N,
      })
    } else {
      hmUI.createWidget(hmUI.widget.IMG, { x: 212, y: 147, src: mid.label, show_level: N })
    }
    if (mid.extra === 'hilo') {
      num(Object.assign({ x: 212, w: 80, align_h: hmUI.align.RIGHT, type: hmUI.data_type.WEATHER_HIGH, negative_image: 'c_neg.png' }, u('c_deg.png')))
      hmUI.createWidget(hmUI.widget.IMG, { x: 292, y: 190, src: 'c_sl.png', show_level: N })
      num(Object.assign({ x: 316, w: 72, type: hmUI.data_type.WEATHER_LOW, negative_image: 'c_neg.png' }, u('c_deg.png')))
    } else {
      const extra = {}
      if (mid.extra === 'dot') extra.dot_image = 'c_dot.png'
      if (mid.extra === 'col') extra.dot_image = 'c_col.png'
      if (mid.extra === 'neg') extra.negative_image = 'c_neg.png'
      num(Object.assign({ type: hmUI.data_type[mid.dt] }, extra, u(mid.unit)))
    }

    // ---------- weather row (orange) ----------
    hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
      x: 14, y: 284, image_array: seq('wb', 29), image_length: 29, type: hmUI.data_type.WEATHER_CURRENT, show_level: N,
    })
    hmUI.createWidget(hmUI.widget.TEXT_IMG, {
      x: 222, y: 284, w: 160, h: 77, font_array: seq('t'), h_space: 0, align_h: hmUI.align.RIGHT,
      negative_image: 't_neg.png', invalid_image: 't_none.png', type: hmUI.data_type.WEATHER_CURRENT,
      unit_en: 't_deg.png', unit_sc: 't_deg.png', unit_tc: 't_deg.png', show_level: N,
    })

    // ---------- bottom slot + bar ----------
    const bType = bot === 'cal' ? hmUI.data_type.CAL : hmUI.data_type.STEP
    const bUnit = bot === 'cal' ? 's_kcal.png' : 's_unit.png'
    hmUI.createWidget(hmUI.widget.TEXT_IMG, {
      x: 16, y: 384, w: 300, h: 55, font_array: seq('s'), h_space: 0,
      unit_en: bUnit, unit_sc: bUnit, unit_tc: bUnit, type: bType, show_level: N,
    })
    hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
      x: 0, y: 441, image_array: seq('bar', 21), image_length: 21, type: bType, show_level: N,
    })

    // ---------- tap zones ----------
    zone(4, 12, 200, 138, () => {
      accent = (accent + 1) % ACC.length
      hours.forEach((w, i) => w.setProperty(hmUI.prop.VISIBLE, i === accent))
      setInt('zuny_accent', accent)
    })
    zone(4, 156, 200, 128, () => launch('timer'))
    zone(208, 36, 178, 74, () => launch('calendar'))
    zone(204, 110, 140, 38, () => launch('alarm'))
    zone(208, 150, 178, 126, () => launch(mid.app))
    zone(8, 284, 376, 90, () => launch('weather'))
    zone(10, 380, 376, 70, () => launch('steps'))
  },
  onInit() {},
  onDestroy() {},
})
