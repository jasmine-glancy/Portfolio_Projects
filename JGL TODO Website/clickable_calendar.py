"""Overrides the HTML calendar to make the days clickable"""
import calendar
from datetime import date
from flask_login import current_user
from helpers import task_lookup


class ClickableHTMLCalendar(calendar.HTMLCalendar):
    """Reformatting recommended by CoPilot for clickable days"""
    
    def formatday(self, day, month, year, weekday):
        """Formats days to have clickable dates and loads in task boxes"""
        
        today = date.today()
        
        task_bank = {}
        if current_user.is_authenticated:
            for day_iter in range(1, calendar.monthrange(year, month)[1] + 1):
                # Format each task for display
                tasks = task_lookup(month, day_iter, year)
                task_html = self.buildtasklist(month, day_iter, year)
                day_date = f"{month}/{day_iter}/{year}"
                task_bank[day_date] = task_html
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            day_date = f"{month}/{day}/{year}"
            task_html = task_bank.get(day_date, "")
            if day == today.day and month == today.month and year == today.year:
                if not task_html:
                    # If today's date doesn't have tasks, set class as no_tasks
                    html_string = '<td class="{} today no_tasks"><a href="/day_view/{}/{}/{}">{}</a></td>'
                    return html_string.format(
                        self.cssclasses[weekday], month, day, year, day)
                else:
                    html_string = '<td class="{} today contains_tasks"><a href="/day_view/{}/{}/{}">{}</a>{}</td>'
                    return html_string.format(
                        self.cssclasses[weekday], month, day, year, day, task_html)
            else:
                if not task_html:
                    # If any other date doesn't have tasks, set class as no_tasks
                    html_string = '<td class="{} no_tasks"><a href="/day_view/{}/{}/{}">{}</a></td>'
                    return html_string.format(
                        self.cssclasses[weekday], month, day, year, day)
                else:
                    html_string = '<td class="{} contains_tasks"><a href="/day_view/{}/{}/{}">{}</a>{}</td>'
                    return html_string.format(
                        self.cssclasses[weekday], month, day, year, day, task_html)
                    
    def formatweek(self, theweek, month, year):
        """Formats a week into a table row"""
        week_html = '<tr>'
        for d, wd in theweek:
            week_html += self.formatday(d, month, year, wd)
        week_html += '</tr>'
        return week_html    
    
                  
    def formatmonth(self, theyear, themonth, withyear=True):
        """Formats a month into an HTML table"""
        month_html = '<table border="0" cellpadding="0" cellspacing="0" class="month">'
        month_html += f'<tr><th colspan="7">{self.formatmonthname(theyear, themonth, withyear=withyear)}</th></tr>'
        month_html += self.formatweekheader()
        for week in self.monthdays2calendar(theyear, themonth):
            month_html += self.formatweek(week, themonth, theyear)
        month_html += '</table>'
        return month_html
    
    
    def buildtasklist(self, month, day, year):
        """Builds the HTML for the task list for a given day"""

        # Format each task for display
        tasks = task_lookup(month, day, year)
        
        task_list_html = '<div class="task_boxes">'
        close_div = "</div>"
        
        print(len(tasks))
  
        box_count = 0
        for task in tasks:

            if box_count == 0:
                task_list_html += '<div class="row_1">'
            elif box_count == 4:
                task_list_html += '<div class="row_2">' 
            elif box_count >= 4 and box_count % 4 == 0:
                # After the first 8 boxes, make extended rows
                task_list_html += '<div class="extended_row">'
                
                
            # Builds a box of color for each task
            task_list_html += f'<div class="task_box" style="background-color: {task.task_color};">'
            
            # Allows the user to see task info on hover
            task_list_html += f'<div class="tooltip"><div class="tooltiptext"> {task.task_name}</div></div>'
                
            box_count += 1 
            
        if box_count % 4 == 0 and box_count > 0 and box_count <= 8:
            task_list_html += close_div
            
        task_list_html += close_div
        
        return task_list_html
            
