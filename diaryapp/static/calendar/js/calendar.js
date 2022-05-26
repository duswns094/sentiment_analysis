
    let date = new Date();

  const renderCalender = () => {
    const viewYear = date.getFullYear();
    const viewMonth = date.getMonth();
    const monthNameLong = date.toLocaleString("en-US", { month: "long" });
    document.querySelector('.year-month').textContent = `${viewYear} ${monthNameLong}`;

    const prevLast = new Date(viewYear, viewMonth, 0);
    const thisLast = new Date(viewYear, viewMonth + 1, 0);

    const PLDate = prevLast.getDate();
    const PLDay = prevLast.getDay();

    const TLDate = thisLast.getDate();
    const TLDay = thisLast.getDay();

    const prevDates = [];
    const thisDates = [...Array(TLDate + 1).keys()].slice(1);
    const nextDates = [];

    if (PLDay !== 6) {
      for (let i = 0; i < PLDay + 1; i++) {
        prevDates.unshift(PLDate - i);
      }
    }

    for (let i = 1; i < 7 - TLDay; i++) {
      nextDates.push(i);
    }

    const dates = prevDates.concat(thisDates, nextDates);
    const firstDateIndex = dates.indexOf(1);
    const lastDateIndex = dates.lastIndexOf(TLDate);

    dates.forEach((date, i) => {

      const condition = i >= firstDateIndex && i < lastDateIndex + 1
                        ? 'this'
                        : 'other';
      var color = ''
      for(let j=0; j<diaries.length;j++){

        if(new Date(diaries[j]['real_date']).getDate() == date
          && new Date(diaries[j]['real_date']).getFullYear() == viewYear
          && new Date(diaries[j]['real_date']).getMonth() == (viewMonth)){
          color = diaries[j]['color'] ;
          console.log(color);
        };
      };
      dates[i] = `<div class="date" id="${date}" style="border:10px solid #${color};"><span class=${condition}>${date}

      </span></div>`;
    });

    document.querySelector('.dates').innerHTML = dates.join('');

    const today = new Date();
    if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
      for (let date of document.querySelectorAll('.this')) {
        if (+date.innerText === today.getDate()) {
          date.classList.add('today');
          break;
        }
      }
    }
  };

  renderCalender();

  const prevMonth = () => {
    date.setDate(1);
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
  }

  const nextMonth = () => {
    date.setDate(1);
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
  }

  const goToday = () => {
    date = new Date();
    renderCalender();
  };