const API_BASE_URL = 'http://127.0.0.1:8000';

let accessToken = localStorage.getItem('access_token');
let currentCity = 'Astana';

function getWeatherTheme(code, isDay = true) {
    if (code === 0) {
        return isDay ? 'weather-clear-day' : 'weather-clear-night';
    } else if (code === 1 || code === 2) {
        return isDay ? 'weather-partly-cloudy-day' : 'weather-partly-cloudy-night';
    } else if (code === 3) {
        return isDay ? 'weather-cloudy-day' : 'weather-cloudy-night';
    } else if (code === 45 || code === 48) {
        return 'weather-fog';
    } else if (code >= 51 && code <= 67) {
        return 'weather-rain';
    } else if ((code >= 71 && code <= 77) || code === 85 || code === 86) {
        return 'weather-snow';
    } else if (code >= 95) {
        return 'weather-storm';
    }

    return isDay ? 'weather-clear-day' : 'weather-clear-night';
}

function applyWeatherTheme(weatherCode, isDay) {
    document.body.classList.remove(
        'weather-clear-day',
        'weather-clear-night',
        'weather-cloudy-day',
        'weather-cloudy-night',
        'weather-rain',
        'weather-snow',
        'weather-fog',
        'weather-storm',
        'weather-partly-cloudy-day',
        'weather-partly-cloudy-night'
    );

    const theme = getWeatherTheme(weatherCode, isDay);
    document.body.classList.add(theme);
    console.log('Applied theme:', theme);
}

function applyThemeByCondition(conditionType, isDay = true) {
    const type = (conditionType || '').toUpperCase();

    if (type.includes('THUNDER')) {
        document.body.className = '';
        document.body.classList.add('weather-storm');
        return;
    }
    if (type.includes('SNOW') || type.includes('BLIZZARD') || type.includes('SLEET')) {
        document.body.className = '';
        document.body.classList.add('weather-snow');
        return;
    }
    if (type.includes('RAIN') || type.includes('DRIZZLE') || type.includes('SHOWER')) {
        document.body.className = '';
        document.body.classList.add('weather-rain');
        return;
    }
    if (type.includes('FOG') || type.includes('MIST') || type.includes('HAZE')) {
        document.body.className = '';
        document.body.classList.add('weather-fog');
        return;
    }
    if (type.includes('CLOUD')) {
        document.body.className = '';
        document.body.classList.add(isDay ? 'weather-cloudy-day' : 'weather-cloudy-night');
        return;
    }

    document.body.className = '';
    document.body.classList.add(isDay ? 'weather-clear-day' : 'weather-clear-night');
}

function getWeatherIcon(code, isDay = true) {
    const icons = {
        0: '☀️',
        1: '🌤️',
        2: '⛅',
        3: '☁️',
        45: '🌫️',
        48: '🌫️',
        51: '🌦️',
        61: '🌧️',
        71: '🌨️',
        95: '⛈️',
    };

    if (!isDay && (code === 0 || code === 1)) {
        return '🌙';
    }

    return icons[code] || '🌤️';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
        return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
        return 'Tomorrow';
    }

    return `${days[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]}`;
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return `${date.getHours().toString().padStart(2, '0')}:00`;
}

function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    const errorText = document.getElementById('errorText');

    errorText.textContent = message;
    errorContainer.style.display = 'block';

    document.getElementById('currentWeather').style.display = 'none';
    document.getElementById('hourlyForecast').style.display = 'none';
    document.getElementById('dailyForecast').style.display = 'none';
}

function hideError() {
    document.getElementById('errorContainer').style.display = 'none';
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function toNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
}

function safeText(value, fallback = 'No data') {
    if (value === undefined || value === null || value === '') return fallback;
    return value;
}

function formatWindDirection(direction) {
    if (!direction) return '';
    const map = {
        NORTH: 'north',
        SOUTH: 'south',
        EAST: 'east',
        WEST: 'west',
        NORTHEAST: 'north-east',
        NORTHWEST: 'north-west',
        SOUTHEAST: 'south-east',
        SOUTHWEST: 'south-west',
        NORTH_NORTHEAST: 'north-north-east',
        NORTH_NORTHWEST: 'north-north-west',
        EAST_NORTHEAST: 'east-north-east',
        EAST_SOUTHEAST: 'east-south-east',
        SOUTH_SOUTHEAST: 'south-south-east',
        SOUTH_SOUTHWEST: 'south-south-west',
        WEST_NORTHWEST: 'west-north-west',
        WEST_SOUTHWEST: 'west-south-west'
    };
    return map[direction] || String(direction).toLowerCase().replaceAll('_', '-');
}

function getValue(obj, path, fallback = undefined) {
    try {
        return path.split('.').reduce((acc, key) => acc?.[key], obj) ?? fallback;
    } catch {
        return fallback;
    }
}

function unwrapData(payload) {
    if (payload && typeof payload === 'object' && payload.success === true && payload.data !== undefined) {
        return payload.data;
    }
    return payload;
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

async function login(username, password) {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('scope', 'me weather');

        const response = await fetch(`${API_BASE_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Invalid username or password');
        }

        const data = await response.json();
        accessToken = data.access_token;
        localStorage.setItem('access_token', accessToken);

        console.log('Token successfully saved:', accessToken.substring(0, 20) + '...');

        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

async function signup(username, email, password, fullName = null) {
    try {
        const requestBody = {
            username: username,
            email: email,
            password: password
        };

        if (fullName && fullName.trim()) {
            requestBody.full_name = fullName;
        }

        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Registration error');
        }

        const data = await response.json();
        console.log('Registration successful:', data);

        return data;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

function logout() {
    accessToken = null;
    localStorage.removeItem('access_token');
    window.location.href = '/static/html/login.html';
}

async function getCurrentUser() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        });

        if (response.status === 401) {
            logout();
            return null;
        }

        if (!response.ok) {
            throw new Error('Error fetching user data');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function getCurrentWeather(city) {
    console.log('Requesting current weather for:', city);
    console.log('Using token:', accessToken ? accessToken.substring(0, 20) + '...' : 'MISSING');

    const response = await fetch(
        `${API_BASE_URL}/weather/current?city=${encodeURIComponent(city)}`,
        {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        }
    );

    if (!response.ok) {
        console.error('Weather request error:', response.status, response.statusText);
        throw new Error('Failed to fetch weather data');
    }

    const data = await response.json();
    return unwrapData(data);
}

async function getHourlyWeather(city) {
    const response = await fetch(
        `${API_BASE_URL}/weather/hourly-12?city=${encodeURIComponent(city)}`,
        {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        }
    );

    if (!response.ok) {
        throw new Error('Failed to fetch hourly forecast');
    }

    const data = await response.json();
    return unwrapData(data);
}

async function getWeeklyWeather(city) {
    const response = await fetch(
        `${API_BASE_URL}/weather/forecast-7days?city=${encodeURIComponent(city)}`,
        {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        }
    );

    if (!response.ok) {
        throw new Error('Failed to fetch weekly forecast');
    }

    const data = await response.json();
    return unwrapData(data);
}

function displayCurrentWeather(data, hourlyData = []) {
    const temp = toNumber(data.temperature);
    const feelsLike = toNumber(data.feels_like ?? data.apparent_temperature);
    const humidity = toNumber(data.humidity ?? hourlyData?.[0]?.humidity);
    const pressure = toNumber(data.pressure);

    document.getElementById('cityName').textContent = data.city || currentCity;
    document.getElementById('currentTemp').textContent = temp !== null ? `${Math.round(temp)}°` : '--';
    document.getElementById('weatherDescription').textContent = safeText(data.condition ?? data.description);
    document.getElementById('feelsLike').textContent = feelsLike !== null ? `${Math.round(feelsLike)}°` : '--';
    const windSpeed = toNumber(data.wind_speed);
    const windDirection = formatWindDirection(data.wind_direction || hourlyData?.[0]?.wind_direction);
    document.getElementById('windSpeed').textContent = windSpeed !== null
        ? `${Math.round(windSpeed)} m/s${windDirection ? ` ${windDirection}` : ''}`
        : '--';
    document.getElementById('humidity').textContent = humidity !== null ? `${humidity}%` : '--';
    document.getElementById('pressure').textContent = pressure !== null ? `${Math.round(pressure * 0.750062)} mmHg` : '--';

    const iconNode = document.getElementById('weatherIcon');
    if (data.icon) {
        iconNode.innerHTML = `<img src="${data.icon}" alt="weather" style="width:72px;height:72px;vertical-align:middle;"/>`;
    } else {
        const icon = getWeatherIcon(data.weather_code, data.is_day);
        iconNode.textContent = icon;
    }

    if (data.weather_code !== undefined && data.weather_code !== null) {
        applyWeatherTheme(data.weather_code, data.is_day);
    } else {
        applyThemeByCondition(data.condition_type, data.is_day);
    }

    document.getElementById('currentWeather').style.display = 'block';
}

function displayHourlyWeather(data) {
    const container = document.getElementById('hourlyContainer');
    container.innerHTML = '';

    data.forEach(hour => {
        const hourDiv = document.createElement('div');
        hourDiv.className = 'hourly-item';

        const icon = hour.icon
            ? `<img src="${hour.icon}" alt="weather" style="width:28px;height:28px;vertical-align:middle;"/>`
            : getWeatherIcon(hour.weather_code, hour.is_day);

        hourDiv.innerHTML = `
            <div class="hourly-time">${formatTime(hour.time)}</div>
            <div class="hourly-icon">${icon}</div>
            <div class="hourly-temp">${toNumber(hour.temperature) !== null ? Math.round(hour.temperature) + '°' : '--'}</div>
        `;

        container.appendChild(hourDiv);
    });

    document.getElementById('hourlyForecast').style.display = 'block';
}

function displayDailyWeather(data) {
    const list = Array.isArray(data)
        ? data
        : (Array.isArray(data?.forecastDays) ? data.forecastDays : []);

    const container = document.getElementById('dailyContainer');
    container.innerHTML = '';

    list.forEach(day => {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'daily-item';

        const iconDay = day.icon_day || getValue(day, 'daytimeForecast.weatherCondition.iconBaseUri');
        const icon = iconDay
            ? `<img src="${iconDay}" alt="weather" style="width:34px;height:34px;vertical-align:middle;"/>`
            : getWeatherIcon(day.weather_code);

        const dayDescription =
            day.description ||
            day.condition_day ||
            getValue(day, 'daytimeForecast.weatherCondition.description.text') ||
            'No data';

        const tMax = toNumber(
            day.temperature_max ??
            day.max_temp ??
            day.temperature_2m_max ??
            getValue(day, 'maxTemperature.degrees')
        );

        const tMin = toNumber(
            day.temperature_min ??
            day.min_temp ??
            day.temperature_2m_min ??
            getValue(day, 'minTemperature.degrees')
        );

        const dateValue = day.date || getValue(day, 'interval.startTime');

        dayDiv.innerHTML = `
            <div class="daily-date">${dateValue ? formatDate(dateValue) : 'No date'}</div>
            <div class="daily-icon">${icon}</div>
            <div class="daily-description">${dayDescription}</div>
            <div class="daily-temp">
                <span class="temp-high">${tMax !== null ? Math.round(tMax) + '°' : '--'}</span>
                <span class="temp-low">${tMin !== null ? Math.round(tMin) + '°' : '--'}</span>
            </div>
        `;

        container.appendChild(dayDiv);
    });

    document.getElementById('dailyForecast').style.display = 'block';
}

async function loadWeather(city) {
    showLoading();
    hideError();
    currentCity = city;

    try {
        const [current, hourly, daily] = await Promise.all([
            getCurrentWeather(city),
            getHourlyWeather(city),
            getWeeklyWeather(city)
        ]);

        displayCurrentWeather(current, hourly);
        displayHourlyWeather(hourly);
        displayDailyWeather(daily);

    } catch (error) {
        console.error('Weather loading error:', error);
        showError(`Failed to load data for city "${city}". Please check the city name.`);
    } finally {
        hideLoading();
    }
}

if (window.location.pathname.includes('signup.html') || document.getElementById('signupForm')) {
    const signupForm = document.getElementById('signupForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const fullName = document.getElementById('fullName').value;

            errorMessage.classList.remove('show');
            successMessage.classList.remove('show');

            if (password !== confirmPassword) {
                errorMessage.textContent = 'Passwords do not match';
                errorMessage.classList.add('show');
                return;
            }

            if (password.length < 6) {
                errorMessage.textContent = 'Password must be at least 6 characters long';
                errorMessage.classList.add('show');
                return;
            }

            try {
                await signup(username, email, password, fullName);

                successMessage.textContent = 'Registration successful! Redirecting to login...';
                successMessage.classList.add('show');

                setTimeout(() => {
                    window.location.href = '/static/html/login.html';
                }, 2000);
            } catch (error) {
                errorMessage.textContent = error.message;
                errorMessage.classList.add('show');
            }
        });
    }
}

if (window.location.pathname.includes('login.html') || document.getElementById('loginForm')) {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            errorMessage.classList.remove('show');

            try {
                const data = await login(username, password);
                console.log('Login successful, token saved');

                setTimeout(() => {
                    window.location.href = '/static/html/main.html';
                }, 100);
            } catch (error) {
                errorMessage.textContent = error.message;
                errorMessage.classList.add('show');
            }
        });
    }
}

if (window.location.pathname.includes('main.html') || document.getElementById('citySearch')) {
    console.log('Loading main page...');

    accessToken = localStorage.getItem('access_token');
    console.log('Token from localStorage:', accessToken ? accessToken.substring(0, 20) + '...' : 'NOT FOUND');

    if (!accessToken) {
        console.warn('Token not found, redirecting to login');
        window.location.href = '/static/html/login.html';
    } else {
        console.log('Token found, loading data...');

        getCurrentUser().then(user => {
            if (user) {
                console.log('User loaded:', user.username);
                document.getElementById('userName').textContent = user.username;
            } else {
                console.error('Failed to load user');
            }
        }).catch(err => {
            console.error('User loading error:', err);
        });

        document.getElementById('logoutBtn').addEventListener('click', logout);

        const citySearch = document.getElementById('citySearch');
        const searchBtn = document.getElementById('searchBtn');

        function searchCity() {
            const city = citySearch.value.trim();
            if (city) {
                loadWeather(city);
            }
        }

        searchBtn.addEventListener('click', searchCity);

        citySearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchCity();
            }
        });

        loadWeather(currentCity);
    }
}
