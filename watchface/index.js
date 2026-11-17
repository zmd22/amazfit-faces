const L = {
  big_w: 100, big_h: 170, hour_x: 170, hour_y: 18, min_x: 170, min_y: 200,
  ring_x: 64, ring_r: 46, ring_w: 10,
  bat_y: 66, step_y: 176, heart_y: 284, wx_y: 392,
  date_y: 392, week_x: 150, month_x: 248, day_x: 312, sm_h: 30,
}
const YEL = 0xf0f014
const arr = (p) => [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => `${p}_${i}.png`)
const BIG = arr('big'), AOD = arr('aod'), SM = arr('sm'), DT = arr('dt')
const WK = [0, 1, 2, 3, 4, 5, 6].map((i) => `wk_${i}.png`)
const WX = Array.from({ length: 29 }, (_, i) => `wx_${i}.png`)
const NORMAL = hmUI.show_level.ONLY_NORMAL
const ONLY_AOD = hmUI.show_level.ONLY_AOD

function num(type, y, extra) {
  hmUI.createWidget(hmUI.widget.TEXT_IMG, Object.assign({
    x: 4, y, w: 120, h: L.sm_h, font_array: SM, h_space: 0,
    align_h: hmUI.align.CENTER_H, type, show_level: NORMAL,
    invalid_image: 'sm_none.png',
  }, extra || {}))
}

function ring(cy, type) {
  hmUI.createWidget(hmUI.widget.ARC_PROGRESS, {
    center_x: L.ring_x, center_y: cy, radius: L.ring_r - L.ring_w / 2,
    start_angle: 0, end_angle: 360, color: YEL, line_width: L.ring_w,
    type, show_level: NORMAL,
  })
}

function time(src) {
  return {
    hour_zero: 1, hour_startX: L.hour_x, hour_startY: L.hour_y, hour_array: src, hour_space: 0,
    minute_zero: 1, minute_startX: L.min_x, minute_startY: L.min_y, minute_array: src, minute_space: 0,
    minute_follow: 0,
  }
}

WatchFace({
  build() {
    hmUI.createWidget(hmUI.widget.IMG, { x: 0, y: 0, src: 'bg.png', show_level: NORMAL })
    hmUI.createWidget(hmUI.widget.IMG, { x: 0, y: 0, src: 'aod_bg.png', show_level: ONLY_AOD })

    ring(L.bat_y, hmUI.data_type.BATTERY)
    ring(L.step_y, hmUI.data_type.STEP)

    hmUI.createWidget(hmUI.widget.IMG_TIME, Object.assign(time(BIG), { show_level: NORMAL }))
    hmUI.createWidget(hmUI.widget.IMG_TIME, Object.assign(time(AOD), { show_level: ONLY_AOD }))

    num(hmUI.data_type.BATTERY, L.bat_y - 15, { unit_en: 'sm_pct.png', unit_sc: 'sm_pct.png', unit_tc: 'sm_pct.png' })
    num(hmUI.data_type.STEP, L.step_y - 15)
    num(hmUI.data_type.HEART, L.heart_y - 20)

    hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
      x: L.ring_x - 25, y: L.wx_y - 36, image_array: WX, image_length: WX.length,
      type: hmUI.data_type.WEATHER_CURRENT, show_level: NORMAL,
    })
    num(hmUI.data_type.WEATHER_CURRENT, L.wx_y + 6, {
      negative_image: 'sm_minus.png',
      unit_en: 'sm_deg.png', unit_sc: 'sm_deg.png', unit_tc: 'sm_deg.png',
    })

    hmUI.createWidget(hmUI.widget.IMG_WEEK, {
      x: L.week_x, y: L.date_y, week_en: WK, week_sc: WK, week_tc: WK,
      show_level: NORMAL | ONLY_AOD,
    })
    hmUI.createWidget(hmUI.widget.IMG_DATE, {
      month_startX: L.month_x, month_startY: L.date_y, month_zero: 1, month_space: 0,
      month_en_array: DT, month_sc_array: DT, month_tc_array: DT,
      month_unit_en: 'dt_sep.png', month_unit_sc: 'dt_sep.png', month_unit_tc: 'dt_sep.png',
      day_startX: L.day_x, day_startY: L.date_y, day_zero: 1, day_space: 0, day_follow: 0,
      day_en_array: DT, day_sc_array: DT, day_tc_array: DT,
      show_level: NORMAL | ONLY_AOD,
    })
  },
  onInit() {},
  onDestroy() {},
})
