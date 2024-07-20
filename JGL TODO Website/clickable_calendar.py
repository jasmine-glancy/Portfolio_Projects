"""Overrides the HTML calendar to make the days clickable"""
import calendar
from datetime import date


class ClickableHTMLCalendar(calendar.HTMLCalendar):
    """Reformatting recommended by CoPilot for clickable days"""
    
    def formatday(self, day, month, year, weekday):
        
        today = date.today()
        if day == 0:
            return "<td class='noday'>&nbsp;</td>"
        elif day == today:
            return f"<td class='{self.cssclasses[weekday]} today'><a href='/day_view/{month}/{day}/{year}'>{day}</a></td>"
        else:
            return f"<td class='{self.cssclasses[weekday]}'><a href='/day_view/{month}/{day}/{year}'>{day}</a></td>"

    def formatmonth(self, theyear, themonth, withyear=True):
        html_strings = []
        c = html_strings.append
        c("<table border='0' cellpadding='0' cellspacing='0' class='month'>")
        c("\n")
        c(self.formatmonthname(theyear, themonth, withyear=withyear))
        c("\n")
        c(self.formatweekheader())
        c("\n")
        for week in self.monthdays2calendar(theyear, themonth):
            c(self.formatweek(theyear, themonth, week))
            c("\n")
        c("</table>")
        c("\n")
        return "".join(html_strings)
    
    def formatweek(self, theyear, themonth, theweek):
        s = "".join(self.formatday(d, themonth, theyear, wd) for (d, wd) in theweek)
        return f"<tr>{s}</tr>"