/**
 * VibeLayer Brand Kit
 * Brand consistency scoring and analysis algorithms
 */

export interface ColorPalette {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  text: string;
}

export interface BrandKit {
  id: string;
  name: string;
  colors: ColorPalette;
  fonts: {
    primary: string;
    secondary: string;
  };
  logo?: string;
  guidelines: {
    colorUsage: string[];
    fontUsage: string[];
    tonality: 'professional' | 'casual' | 'energetic' | 'calm';
  };
}

export interface BrandScore {
  overall: number;
  colorConsistency: number;
  fontConsistency: number;
  tonalityMatch: number;
  details: {
    colorIssues: string[];
    fontIssues: string[];
    tonalityIssues: string[];
  };
}

export class BrandAnalyzer {
  private brandKit: BrandKit;

  constructor(brandKit: BrandKit) {
    this.brandKit = brandKit;
  }

  analyzeContent(content: {
    colors: string[];
    fonts: string[];
    tone: string;
  }): BrandScore {
    const colorScore = this.analyzeColorConsistency(content.colors);
    const fontScore = this.analyzeFontConsistency(content.fonts);
    const tonalityScore = this.analyzeTonalityMatch(content.tone);

    const overall = (colorScore.score + fontScore.score + tonalityScore.score) / 3;

    return {
      overall,
      colorConsistency: colorScore.score,
      fontConsistency: fontScore.score,
      tonalityMatch: tonalityScore.score,
      details: {
        colorIssues: colorScore.issues,
        fontIssues: fontScore.issues,
        tonalityIssues: tonalityScore.issues,
      },
    };
  }

  private analyzeColorConsistency(colors: string[]): { score: number; issues: string[] } {
    const issues: string[] = [];
    let score = 1.0;

    const brandColors = Object.values(this.brandKit.colors);
    const unmatchedColors = colors.filter(color => 
      !brandColors.some(brandColor => this.colorsMatch(color, brandColor))
    );

    if (unmatchedColors.length > 0) {
      score -= unmatchedColors.length * 0.2;
      issues.push(`Non-brand colors detected: ${unmatchedColors.join(', ')}`);
    }

    return { score: Math.max(0, score), issues };
  }

  private analyzeFontConsistency(fonts: string[]): { score: number; issues: string[] } {
    const issues: string[] = [];
    let score = 1.0;

    const brandFonts = [this.brandKit.fonts.primary, this.brandKit.fonts.secondary];
    const unmatchedFonts = fonts.filter(font => 
      !brandFonts.some(brandFont => font.toLowerCase().includes(brandFont.toLowerCase()))
    );

    if (unmatchedFonts.length > 0) {
      score -= unmatchedFonts.length * 0.3;
      issues.push(`Non-brand fonts detected: ${unmatchedFonts.join(', ')}`);
    }

    return { score: Math.max(0, score), issues };
  }

  private analyzeTonalityMatch(tone: string): { score: number; issues: string[] } {
    const issues: string[] = [];
    let score = 1.0;

    const expectedTonality = this.brandKit.guidelines.tonality;
    const toneMatch = this.getTonalityScore(tone, expectedTonality);

    if (toneMatch < 0.7) {
      score = toneMatch;
      issues.push(`Tone mismatch: expected ${expectedTonality}, detected tone doesn't align`);
    }

    return { score, issues };
  }

  private colorsMatch(color1: string, color2: string): boolean {
    // Simplified color matching - in production would use proper color space comparison
    return color1.toLowerCase() === color2.toLowerCase();
  }

  private getTonalityScore(content: string, expectedTonality: string): number {
    // Simplified tonality analysis - in production would use NLP
    const contentLower = content.toLowerCase();
    
    switch (expectedTonality) {
      case 'professional':
        return contentLower.includes('professional') || contentLower.includes('business') ? 0.9 : 0.5;
      case 'casual':
        return contentLower.includes('casual') || contentLower.includes('friendly') ? 0.9 : 0.5;
      case 'energetic':
        return contentLower.includes('energy') || contentLower.includes('dynamic') ? 0.9 : 0.5;
      case 'calm':
        return contentLower.includes('calm') || contentLower.includes('peaceful') ? 0.9 : 0.5;
      default:
        return 0.7;
    }
  }
}

export const createBrandAnalyzer = (brandKit: BrandKit): BrandAnalyzer => {
  return new BrandAnalyzer(brandKit);
};

export const getDefaultBrandKit = (): BrandKit => ({
  id: 'default',
  name: 'VibeLayer Default',
  colors: {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    accent: '#06b6d4',
    background: '#ffffff',
    text: '#1f2937',
  },
  fonts: {
    primary: 'Inter',
    secondary: 'JetBrains Mono',
  },
  guidelines: {
    colorUsage: ['Use primary for main actions', 'Use secondary for highlights'],
    fontUsage: ['Use primary for body text', 'Use secondary for code'],
    tonality: 'professional',
  },
});