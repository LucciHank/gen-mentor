# GenMentor Onboarding Mockups - Cụm A

Bộ 7 màn hình onboarding hoàn chỉnh theo Apple HIG style, tối giản và hiện đại.

## 🎯 Mục tiêu UX

1. **User luôn biết việc cần làm tiếp theo** - Progress bar và CTA rõ ràng
2. **User luôn biết mình đang học theo kế hoạch nào** - Sidebar navigation nhất quán
3. **Agent giúp quyết định, không cướp quyền kiểm soát** - AI suggestions có thể dismiss
4. **Mỗi màn hình chỉ có 1 mục tiêu chính** - Form sections tách biệt rõ ràng
5. **UI sạch, rõ, yên tĩnh, ít nhiễu thị giác** - Apple HIG design system

## 📱 Danh sách màn hình

### Screen 1 - Welcome / Empty State
- **File**: `screen_1_welcome.html`
- **Mục tiêu**: Dẫn user bắt đầu tạo learning path
- **Features**: 
  - Greeting và value proposition
  - 3 benefits chính
  - CTA: "Tạo lộ trình học" + "Xem demo"
  - Agent card có thể dismiss

### Screen 2 - Goal Setup  
- **File**: `screen_2_goal_setup.html`
- **Mục tiêu**: Thu thập mục tiêu học tập
- **Features**:
  - Textarea cho mục tiêu chính
  - Suggested goal chips
  - Target deadline dropdown
  - Current level selection
  - Expected outcome input
  - Form validation

### Screen 3 - Profile Source / CV Upload
- **File**: `screen_3_profile_source.html`
- **Mục tiêu**: Thu thập dữ liệu nền từ CV và skills
- **Features**:
  - Drag & drop CV upload
  - LinkedIn/GitHub connection cards
  - Self-assessment skill tags
  - Agent hint về skip CV option
  - File validation và preview

### Screen 4 - Availability & Preferences
- **File**: `screen_4_availability.html`
- **Mục tiêu**: Thiết lập lịch học và preferences
- **Features**:
  - Sessions per week selection
  - Minutes per session options
  - Weekly schedule grid (7x3)
  - Learning style cards (Video, Reading, Practice, Quiz)
  - Device selection chips
  - Real-time summary calculation

### Screen 5 - AI Extraction Review
- **File**: `screen_5_ai_review.html`
- **Mục tiêu**: User xác nhận AI analysis
- **Features**:
  - AI analysis badge và confidence score
  - Editable personal info grid
  - Current skills với levels
  - Skill gaps list với descriptions
  - Inline editing với save states
  - Learning goals summary

### Screen 6 - Generating Path
- **File**: `screen_6_generating.html`
- **Mục tiêu**: Loading có ích với progress steps
- **Features**:
  - Animated AI icon với pulse effect
  - 5-step progress với real-time updates
  - Countdown timer
  - Skeleton roadmap preview
  - Notification toggle
  - Background processing option

### Screen 7 - Path Generated Success
- **File**: `screen_7_success.html`
- **Mục tiêu**: Celebration và next actions
- **Features**:
  - Success animation và celebration
  - Path summary với stats
  - First week preview lessons
  - Primary CTA: "Bắt đầu hôm nay"
  - Secondary actions: View plans
  - Next steps checklist
  - Auto-redirect timer

## 🎨 Design System

### Colors
- **Primary**: `#007AFF` (System Blue)
- **Background**: `#F7F7F8` (Light Gray)
- **Surface**: `white`
- **Text Primary**: `#1D1D1F` (Near Black)
- **Text Secondary**: `#86868B` (Gray)
- **Border**: `#E5E5E7` (Light Gray)
- **Success**: `#34C759` (Green)
- **Warning**: `#FF9500` (Orange)
- **Danger**: `#FF3B30` (Red)

### Typography
- **Font**: SF Pro Display / Inter fallback
- **H1**: 32px, 700 weight, -0.5px letter-spacing
- **H2**: 20px, 600 weight
- **Body**: 16px, 400 weight
- **Caption**: 14px, 500 weight

### Spacing & Layout
- **Grid**: 8pt base unit
- **Border Radius**: 12px/16px/20px
- **Shadows**: Minimal, prefer borders
- **Padding**: 16px/24px/32px/48px
- **Gaps**: 8px/12px/16px/24px

### Components
- **Buttons**: 12px radius, 16px padding, hover effects
- **Cards**: 16px radius, 1px border, white background
- **Form Inputs**: 12px radius, 16px padding, focus states
- **Chips/Tags**: 16px-20px radius, small padding
- **Progress Bar**: 4px height, rounded, smooth transitions

## 🔄 User Flow

```
Welcome → Goal Setup → Profile Source → Availability → AI Review → Generating → Success
   ↓           ↓            ↓             ↓           ↓          ↓         ↓
 Start      Define       Upload CV     Set Time    Confirm    Wait     Begin
Process     Goals        & Skills      & Style     Data      AI       Learning
```

## 💾 Data Flow

### LocalStorage Keys
- `goalSetup`: Mục tiêu và timeline
- `profileSource`: CV và skills data  
- `availability`: Lịch học và preferences
- `aiReview`: Confirmed AI analysis
- `onboardingCompleted`: Completion flag

### Form Validation
- Required fields highlighted
- Real-time validation feedback
- Disabled submit until valid
- Error states với clear messaging

## 🎭 Agent UX Model

### Agent Appearances
1. **Welcome**: Introductory card (dismissible)
2. **Profile**: Hint about skipping CV
3. **AI Review**: Analysis confidence indicator
4. **Generating**: Progress explanation
5. **Success**: Celebration participation

### Agent Principles
- **Non-intrusive**: Cards, not popups
- **Contextual**: Relevant to current step
- **Dismissible**: User control always
- **Helpful**: Clear value proposition

## 📱 Responsive Design

### Breakpoints
- **Desktop**: 1200px+ (sidebar + main)
- **Tablet**: 768px-1199px (stacked layout)
- **Mobile**: <768px (single column)

### Mobile Adaptations
- Sidebar becomes top navigation
- Grid layouts become single column
- Touch-friendly button sizes
- Simplified interactions

## 🚀 Technical Implementation

### HTML Structure
- Semantic HTML5 elements
- Accessible form labels
- ARIA attributes where needed
- Progressive enhancement

### CSS Features
- CSS Grid và Flexbox
- CSS Custom Properties
- Smooth transitions
- Hover/focus states
- Animation keyframes

### JavaScript Functionality
- Form validation
- LocalStorage persistence
- Progress tracking
- Interactive elements
- Navigation flow

## 🧪 Testing Checklist

### Functionality
- [ ] All forms validate correctly
- [ ] Data persists between screens
- [ ] Navigation works in both directions
- [ ] File upload handles errors
- [ ] Responsive layout works
- [ ] Animations perform smoothly

### Accessibility
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Color contrast ratios
- [ ] Focus indicators
- [ ] Error announcements

### UX Validation
- [ ] Clear next steps at each stage
- [ ] Progress indication works
- [ ] Error states are helpful
- [ ] Success feedback is satisfying
- [ ] Agent interactions feel natural

## 📋 Usage Instructions

1. **Open any screen**: Double-click HTML file
2. **Navigate flow**: Use form submissions or buttons
3. **Test data persistence**: Check browser localStorage
4. **Responsive testing**: Resize browser window
5. **Accessibility testing**: Use keyboard only

## 🔧 Customization

### Branding
- Update colors in CSS custom properties
- Replace logo text in sidebar
- Modify success celebration messages

### Content
- Edit form labels và placeholders
- Update skill categories và options
- Customize agent messages
- Modify success metrics

### Behavior
- Adjust validation rules
- Change animation durations
- Modify auto-redirect timers
- Update progress calculations

---

**Design Philosophy**: Tối giản, dễ dùng, ít lòe xòe, Apple HIG style, agent xuất hiện đúng chỗ không làm phiền, learning path là lớp trải nghiệm phủ lên LMS.