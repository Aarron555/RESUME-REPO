export function generateCopyTemplates(scan, recommendation) {
  return {
    recommendation: `Thanks — I reviewed your Dumb Scan. Based on your answers, I’d start with ${recommendation.recommended_system}.`,
    missingInfo: `Thanks — I can review this, but I need one more detail first: ${(scan.missing_info || ["missing info"])[0]}.`,
    depositAsk: `The best starting point is ${recommendation.recommended_system}. The First Fix is $497 total: $197 starts it and $300 is due when live and tested.`,
    notFit: "Thanks for filling out the Dumb Scan. Based on your answers, I do not think Dumbwork is the right fit yet."
  };
}
