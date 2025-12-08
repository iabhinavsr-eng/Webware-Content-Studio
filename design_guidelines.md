# Design Guidelines: SEO Prompt Library Web Application

## Design Approach
**System-Based Approach** - This is a utility-focused productivity tool requiring clarity, efficiency, and scannable forms. Drawing inspiration from Linear's clean typography and Notion's information hierarchy, combined with Material Design's form patterns for reliability.

## Core Design Principles
1. **Information Clarity**: Form fields must be easily scannable with clear labels
2. **Efficient Workflow**: Minimize friction in tool selection and data entry
3. **Output Readability**: JSON responses must be formatted for easy comprehension
4. **Professional Aesthetic**: Clean, modern interface that inspires confidence

## Typography System

**Primary Font**: Inter (Google Fonts)
- Headings: 600 weight
- Body: 400 weight  
- Labels: 500 weight
- Code/JSON: 'JetBrains Mono' for monospace

**Scale**:
- Page Title: text-3xl (30px)
- Section Headers: text-xl (20px)
- Tool Dropdown Label: text-lg (18px)
- Form Labels: text-sm (14px)
- Input Text: text-base (16px)
- JSON Output: text-sm (14px)

## Layout System

**Spacing Units**: Tailwind units of 2, 4, 6, 8, 12, 16
- Form field gaps: space-y-6
- Section padding: p-8
- Container max-width: max-w-4xl
- Input padding: p-4

**Grid Structure**:
- Single column layout for form clarity
- Full-width tool selector (critical decision point)
- Two-column split for output section (label left, content right on desktop)

## Component Library

### Primary Container
- Centered layout with max-w-4xl
- Background card with subtle border and shadow
- Padding: p-8 on desktop, p-6 on mobile
- Rounded corners: rounded-lg

### Tool Selector Dropdown
- Full width select element
- Large touch target: h-12
- Clear visual hierarchy with icon indicator
- Border: 2px solid for prominence
- Rounded: rounded-lg

### Form Inputs
**Text Inputs**:
- Border: 1px solid with focus ring
- Height: h-12 for single-line
- Padding: px-4 py-3
- Rounded: rounded-md
- Font size: text-base

**Textareas**:
- Minimum height: min-h-[120px]
- Resize: vertical only
- Same padding/border treatment as text inputs
- Clear visual separation between fields

**Labels**:
- Positioned above inputs
- Font weight: 500
- Margin bottom: mb-2
- Include helper text in text-sm text-gray-600

### Submit Button
- Full width on mobile, auto width on desktop (px-12)
- Height: h-12
- Font weight: 600
- Prominent visual treatment
- Position: Centered or right-aligned after form

### Output Display

**JSON Container**:
- Full-width code block
- Background: subtle contrast to main surface
- Border: 1px solid
- Padding: p-6
- Rounded: rounded-lg
- Font: JetBrains Mono
- Max height with scroll: max-h-[600px] overflow-y-auto

**Section Headers**:
- Clear separation with border-t
- Padding: pt-8 mt-8
- Bold, prominent text

## Page Structure

1. **Header Section**
   - App title (text-3xl, font-semibold)
   - Brief description text (text-gray-600)
   - Padding: pb-8 with border-b

2. **Tool Selection**
   - Prominent placement immediately after header
   - Dropdown with all 6 tools listed clearly
   - Space-y-2 for label and select

3. **Input Forms Section**
   - Grouped by input type
   - Common fields first (business info)
   - Advanced fields below with subtle visual separation
   - Space-y-6 between field groups

4. **Output Section** (shown after submission)
   - Clear visual separation from input (pt-12 border-t)
   - Status indicator (success/error)
   - Formatted JSON or raw text display

## Visual Hierarchy

**Primary Actions**: Tool selection and submit button
**Secondary Content**: Form labels and helper text
**Tertiary Content**: Output metadata and timestamps

## Responsive Behavior

**Desktop (lg+)**:
- Max container width: max-w-4xl
- Two-column output display
- Generous spacing (p-8)

**Mobile**:
- Full-width forms
- Stacked layout
- Reduced padding (p-6)
- Larger touch targets maintained

## Accessibility
- All inputs have associated labels
- Focus states clearly visible (ring-2 ring-offset-2)
- Sufficient contrast ratios throughout
- Keyboard navigation fully supported

## Animations
**Minimal and purposeful only**:
- Smooth transitions on focus states (transition-colors duration-200)
- Fade-in for output section (optional)
- No decorative animations