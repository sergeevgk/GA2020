package com.example.easymath;

import static java.lang.Math.PI;
import static java.lang.Math.atan;
import static java.lang.Math.sqrt;

public class Vec {
    public Vec (double x_, double y_) {
        x = x_;
        y = y_;
    }

    public Vec (Vec v) {
        x = v.x;
        y = v.y;
    }

    public void Scale (double val) {
        x *= val;
        y *= val;
    }

    public Vec GetScaled (double val) {
        return new Vec(x * val, y * val);
    }

    public void Translate (double x_, double y_) {
        x += x_;
        y += y_;
    }

    public void Translate (Vec v) {
        x += v.x;
        y += v.y;
    }

    public Vec GetTranslated (double x_, double y_) {
        return new Vec(x + x_, y + y_);
    }

    public Vec GetTranslated (Vec v) {
        return new Vec(x + v.x, y + v.y);
    }

    public Vec GetAdded(Vec v) {
        return new Vec(x + v.x, y + v.y);
    }

    public double GetLength() {
        return sqrt(x * x + y * y);
    }

    public double Multyply(Vec v) {
        return x * v.x + y * v.y;
    }

    public void Normalize () {
        x /= GetLength();
        y /= GetLength();
    }

    public double GetAngleToX(Vec v, boolean to_degrees) {
        Vec radial = new Vec(x - v.x, y - v.y);
        radial.Normalize();
        double res = 0;

        if (-radial.y >= 0) {
            res = Math.acos(radial.x);
        } else {
            res = Math.PI + Math.acos(-radial.x);
        }
        return to_degrees ? Math.toDegrees(res) : res;
    }

    public double x;
    public double y;
}
