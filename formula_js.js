function evaluatePartRemark(PartRemark2, PartRef, degem, PartMat, PartQty) {
  if (PartRemark2.includes("פרזול") || PartMat == "סחורה" || PartQty < 1) {
    return "";
  } else if (PartRemark2.includes("CNC") || PartRemark2.includes("ריפוד")) {
    return "~~";
  } else if (PartRemark2.includes("הזזה") || (degem === 1 && PartRef.includes("דלת"))) {
    return "@";
  } else if (
    PartRemark2.includes("OPK") ||
    PartRef.includes("במה") ||
    ((PartRef.includes("OPK") ||
      PartRef.includes("ק_הזזה") ||
      ((PartRef.includes("עליון") || PartRef.includes("תחתון")) && !PartRef.includes("צוקל") && !PartRef.includes("קושר"))) &&
      degem === 1)
  ) {
    return "%%";
  } else if (PartRef.includes("עומד") || (PartRef.includes("מחיצה") && [1, 2, 3].includes(degem))) {
    return "$";
  } else if ([4, 5, 6, 8, 9, 11, 12].includes(degem) && PartRef.includes("דלת") && !PartRef.includes("ארון")) {
    return "[ - ]";
  } else if ((PartRef.includes("דלת") && (degem === 2 || degem === 3)) || (PartRef.includes("צוקל") && degem === 1 && PartQty == 1)) {
    return "[ ]";
  } else if ((PartRef.includes("קושר") || PartRef.includes("@_@")) && !PartRemark2.includes("פרזול") && [1, 2, 3].includes(degem)) {
    return "@_@";
  } else if ((PartRef.includes("מדפים") || PartRef.includes("מדף")) && [1, 2, 3].includes(degem)) {
    return "&_&";
  } else if (
    (degem === 10 || PartRemark2.includes("מיטות") || PartRef.includes("ראש") || (PartRef.includes("חזית") && !PartRef.includes("מגירה"))) &&
    !["מגירה", "מגרות", "מגירות", "צד_מג", "מג", "מג34", "מג35", "מג40", "מ_תחתונה", "צוקל", "מראה"].includes(PartRef)
  ) {
    return "#";
  } else if (PartRef.includes("מראה") && (PartRemark2.includes("מיטות") || degem === 10)) {
    return "##";
  } else if (PartRef.includes("צוקל") && ![5, 7, 8, 9].includes(degem)) {
    return "###";
  } else if (
    PartRemark2.includes("מגרות") ||
    (PartRef.includes("מגירה") && !PartRef.includes("חזית")) ||
    PartRef.includes("מגרות") ||
    PartRef.includes("מגירות") ||
    PartRef === "צד_מג" ||
    PartRef === "מג" ||
    PartRef === "מג34" ||
    PartRef === "מג35" ||
    PartRef === "מג40"
  ) {
    return "####";
  } else if (PartRef.includes("גירונג")) {
    return "XX";
  } else {
    return "**";
  }
}
