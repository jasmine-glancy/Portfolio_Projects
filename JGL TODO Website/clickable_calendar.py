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
        
        tasks = []
        if current_user.is_authenticated:
            tasks = task_lookup(month, day, year)
            task_html = self.buildtasklist(month, day, year)
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        elif day == today.day and month == today.month and year == today.year:
            
            if tasks == []:
                # If today's date doesn't have tasks, set class as no_tasks
                html_string = '<td class="{} today no_tasks"><a href="/day_view/{}/{}/{}">{}</a></td>'
                return html_string.format(
                    self.cssclasses[weekday], month, day, year, day)
            else:
                html_string = '<td class="{} today contains_tasks"><a href="/day_view/{}/{}/{}">{}</a></td>'
                return html_string.format(
                self.cssclasses[weekday], month, day, year, day, task_html)
        else:
            
            if tasks == []:
                # If any other date doesn't have tasks, set class as no_tasks
                html_string = '<td class="{} no_tasks"><a href="/day_view/{}/{}/{}">{}</a></td>'
                return html_string.format(
                self.cssclasses[weekday], month, day, year, day)

            else:
                html_string = '<td class="{} contains_tasks"><a href="/day_view/{}/{}/{}">{}</a>{}</td>'
                return html_string.format(
                    self.cssclasses[weekday], month, day, year, day, task_html)

    def formatmonth(self, theyear, themonth, withyear=True):
        html_strings = []
        c = html_strings.append
        c('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        c('\n')
        c(self.formatmonthname(theyear, themonth, withyear=withyear))
        c('\n')
        c(self.formatweekheader())
        c('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            c(self.formatweek(theyear, themonth, week))
            c('\n')
        c('</table>')
        c('\n')
        return "".join(html_strings)
    
    def formatweek(self, theyear, themonth, theweek):
        
        # Create a string that represents HTML for all days in a week
        s = "".join(self.formatday(d, themonth, theyear, wd) for (d, wd) in theweek)
        
        return f"<tr>{s}</tr>"
    
    def buildtasklist(self, month, day, year):
        
        # Format each task for display
        tasks = task_lookup(month, day, year)
        
        task_list_html = ""
        task_list_html += '<div class="task_boxes">'
        
        close_div = "</div>"
        
        print(len(tasks))
  
        box_count = 0
        for task in tasks:

            if box_count == 0:
                task_list_html += '<div class="row_1">'
            elif box_count == 4:
                task_list_html += '<div class="row_2">'  
            # Builds a box of color for each task
            task_list_html += f'<div class="task_box" style="background-color: {task.task_color};">'
            
            # Allows the user to see task info on hover
            task_list_html += f'<div class="tooltip"><div class="tooltiptext"> {task.task_name}</div></div>'
                
            box_count += 1 
            
        if box_count % 4 == 0 and box_count > 0 and box_count <= 8:
            task_list_html += close_div
            
        task_list_html += close_div
        
        return task_list_html
            
        # Create a string representation for each task
        
        # Concatenate task representations
            # Create a single string that contains the HTML for all tasks of the day
            # Insert tasks strings into the day's cell
