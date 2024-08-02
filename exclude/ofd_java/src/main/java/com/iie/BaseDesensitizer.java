package com.iie;

/**
 * @param ObjectIn input object type
 * @param ObjectOut output object type
 */
public abstract class BaseDesensitizer<ObjectIn, ObjectOut> {
    public abstract ObjectOut desensitize(ObjectIn object, Object... args);
}
